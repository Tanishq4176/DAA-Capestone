"""End-to-end Mini Courier Planner command line application."""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from src.dijkstra import dijkstra, shortest_path
from src.knapsack import knapsack_select_parcels
from src.sorting import parcel_benefit, sort_parcels_by_priority_and_deadline
from src.tsp import plan_nearest_neighbor_route

ROOT = Path(__file__).resolve().parent

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
    parcels = [Parcel(r["parcel_id"], r["destination"], int(r["weight"]), int(r["value"]), int(r["deadline"]), r["priority"]) for r in rows]
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


def run(capacity: int = 12, parcels_path: Path = ROOT / "datasets/parcels.csv", routes_path: Path = ROOT / "datasets/routes.csv") -> str:
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
    lines = ["MINI COURIER PLANNER", f"Vehicle capacity: {capacity} kg", "", "Prioritized parcels (priority, then earliest deadline):"]
    lines += [f"  {p.parcel_id} -> {p.destination} | {p.priority:<6} | deadline {p.deadline} | {p.weight} kg | benefit {parcel_benefit(p)}" for p in ordered]
    lines += ["", f"Packing plan: {', '.join(p.parcel_id for p in selected) or '(no parcels)'}", f"Total weight: {weight}/{capacity} kg", f"Optimal benefit: {optimum}", f"Unused capacity: {capacity-weight} kg", f"DP table: {len(dp)} x {len(dp[0])}", "", "Shortest paths from warehouse:"]
    distances, previous = dijkstra(graph, "Warehouse")
    for destination in destinations:
        lines.append(f"  {' -> '.join(shortest_path(previous, destination))} | {distances[destination]} km")
    lines += ["", f"Nearest-neighbor route: {' -> '.join(route)}", f"Total route distance: {distance} km"]
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
