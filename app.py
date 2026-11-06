"""End-to-end Mini Courier Planner command line application."""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from src.dijkstra import dijkstra, shortest_path
from src.knapsack import knapsack_select_parcels
from src.sorting import parcel_benefit, sort_parcels_by_priority_and_deadline
from src.tsp import expand_route_with_shortest_paths, plan_nearest_neighbor_route

ROOT = Path(__file__).resolve().parent
AUTHOR = "Tanishq"


@dataclass(frozen=True)
class Parcel:
    parcel_id: str
    destination: str
    weight: int
    value: int
    deadline: int
    priority: str


def load_parcels(path: Path) -> list[Parcel]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    parcels = [
        Parcel(
            r["parcel_id"],
            r["destination"],
            int(r["weight"]),
            int(r["value"]),
            int(r["deadline"]),
            r["priority"],
        )
        for r in rows
    ]
    if len({p.parcel_id for p in parcels}) != len(parcels):
        raise ValueError("parcel_id values must be unique")
    for p in parcels:
        if p.weight <= 0 or p.deadline <= 0 or p.priority not in {"High", "Medium", "Low"}:
            raise ValueError(f"Invalid parcel record: {p}")
    return parcels


def load_graph(path: Path) -> dict[str, dict[str, int]]:
    graph: dict[str, dict[str, int]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            a, b, distance = row["source"], row["destination"], int(row["distance"])
            if a == b or distance < 0:
                raise ValueError(f"Invalid road edge: {row}")
            graph.setdefault(a, {})[b] = distance
            graph.setdefault(b, {})[a] = distance
    return graph


def format_graph(graph: dict[str, dict[str, int]]) -> list[str]:
    lines = ["Road graph (undirected adjacency list, distance in km):"]
    for node in sorted(graph):
        neighbors = ", ".join(f"{nbr}:{dist}" for nbr, dist in sorted(graph[node].items()))
        lines.append(f"  {node}: {neighbors}")
    return lines


def format_dp_table(parcels: list[Parcel], dp: list[list[int]]) -> list[str]:
    header = "cap->" + "".join(f"{c:>5}" for c in range(len(dp[0])))
    lines = [
        "0/1 knapsack DP table (rows = parcels considered, columns = remaining kg):",
        "        " + header,
        f"  {'(none)':<7} " + "".join(f"{value:>5}" for value in dp[0]),
    ]
    for i, parcel in enumerate(parcels, start=1):
        label = parcel.parcel_id
        lines.append(f"  {label:<7} " + "".join(f"{value:>5}" for value in dp[i]))
    return lines


def run(
    capacity: int = 12,
    parcels_path: Path = ROOT / "datasets/parcels.csv",
    routes_path: Path = ROOT / "datasets/routes.csv",
) -> str:
    if capacity < 0:
        raise ValueError("Capacity must be non-negative")
    parcels = load_parcels(parcels_path)
    graph = load_graph(routes_path)
    unknown = {p.destination for p in parcels} - graph.keys()
    if unknown:
        raise ValueError(f"Parcel destinations absent from road graph: {sorted(unknown)}")

    ordered = sort_parcels_by_priority_and_deadline(parcels)
    optimum, selected, dp = knapsack_select_parcels(ordered, capacity)
    weight = sum(p.weight for p in selected)
    destinations = list(dict.fromkeys(p.destination for p in selected))
    route, distance = plan_nearest_neighbor_route(graph, "Warehouse", destinations)
    expanded = expand_route_with_shortest_paths(graph, route)

    lines = [
        "MINI COURIER PLANNER",
        f"Student: {AUTHOR}",
        "Integrated prototype: sorting + 0/1 knapsack DP + Dijkstra + nearest-neighbor TSP",
        f"Vehicle capacity: {capacity} kg",
        f"Parcels file: {parcels_path.name}",
        f"Routes file: {routes_path.name}",
        "",
        *format_graph(graph),
        "",
        "Phase 2 sorting: Python Timsort, key = (-priority_score, deadline).",
        "Timsort is stable, so equal priority+deadline parcels keep input order.",
        "Prioritized parcels (High to Low, then earliest deadline):",
    ]
    lines += [
        f"  {p.parcel_id} -> {p.destination} | {p.priority:<6} | deadline {p.deadline} | {p.weight} kg | benefit {parcel_benefit(p)}"
        for p in ordered
    ]
    lines += [
        "",
        f"Packing plan: {', '.join(p.parcel_id for p in selected) or '(no parcels)'}",
        f"Total weight: {weight}/{capacity} kg",
        f"Optimal benefit: {optimum}",
        f"Unused capacity: {capacity - weight} kg",
        f"DP table size: {len(dp)} rows x {len(dp[0])} columns (O(nC) time and space)",
        "",
        *format_dp_table(ordered, dp),
        "",
        "Shortest paths from warehouse (Dijkstra, non-negative km):",
    ]
    distances, previous = dijkstra(graph, "Warehouse")
    for destination in destinations:
        lines.append(f"  {' -> '.join(shortest_path(previous, destination))} | {distances[destination]} km")
    lines += [
        "",
        f"Nearest-neighbor stop order: {' -> '.join(route)}",
        f"Expanded road path: {' -> '.join(expanded)}",
        f"Total route distance: {distance} km",
        "",
        "Note: nearest-neighbor is a TSP approximation. It is not guaranteed to be a globally shortest tour.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capacity", type=int, default=12)
    parser.add_argument("--parcels", type=Path, default=ROOT / "datasets/parcels.csv")
    parser.add_argument("--routes", type=Path, default=ROOT / "datasets/routes.csv")
    args = parser.parse_args()
    print(run(args.capacity, args.parcels, args.routes), end="")


if __name__ == "__main__":
    main()
