"""Correctness checks for sorting, knapsack, Dijkstra, and routing."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import Parcel, load_graph, load_parcels, run
from src.dijkstra import dijkstra, shortest_path
from src.knapsack import knapsack_select_parcels
from src.sorting import parcel_benefit, sort_parcels_by_priority_and_deadline
from src.tsp import expand_route_with_shortest_paths, plan_nearest_neighbor_route


def test_sorting_priority_then_deadline() -> None:
    parcels = load_parcels(ROOT / "datasets/parcels.csv")
    ordered = sort_parcels_by_priority_and_deadline(parcels)
    ids = [p.parcel_id for p in ordered]
    assert ids[0] == "P02"
    assert ids.index("P04") < ids.index("P09")
    scores = [(p.priority, p.deadline) for p in ordered]
    assert scores == sorted(scores, key=lambda item: ({"High": 0, "Medium": 1, "Low": 2}[item[0]], item[1]))


def test_knapsack_sample_instance() -> None:
    parcels = sort_parcels_by_priority_and_deadline(load_parcels(ROOT / "datasets/parcels.csv"))
    benefit, selected, dp = knapsack_select_parcels(parcels, 12)
    assert benefit == 550
    assert [p.parcel_id for p in selected] == ["P02", "P01", "P04", "P09", "P06"]
    assert sum(p.weight for p in selected) == 12
    assert dp[-1][12] == 550
    assert sum(parcel_benefit(p) for p in selected) == benefit


def test_knapsack_small_capacity() -> None:
    parcels = sort_parcels_by_priority_and_deadline(load_parcels(ROOT / "datasets/parcels.csv"))
    benefit, selected, _ = knapsack_select_parcels(parcels, 3)
    assert benefit == 185
    assert sum(p.weight for p in selected) <= 3


def test_dijkstra_warehouse_paths() -> None:
    graph = load_graph(ROOT / "datasets/routes.csv")
    distances, previous = dijkstra(graph, "Warehouse")
    assert distances["B"] == 2
    assert distances["A"] == 3
    assert shortest_path(previous, "A") == ["Warehouse", "B", "A"]


def test_nearest_neighbor_route() -> None:
    graph = load_graph(ROOT / "datasets/routes.csv")
    route, distance = plan_nearest_neighbor_route(graph, "Warehouse", ["B", "A", "D", "I", "F"])
    assert route[0] == route[-1] == "Warehouse"
    assert distance == 23
    expanded = expand_route_with_shortest_paths(graph, route)
    assert expanded[0] == expanded[-1] == "Warehouse"
    assert "A" in expanded and "I" in expanded


def test_end_to_end_trace() -> None:
    trace = run(12)
    assert "Student: Tanishq" in trace
    assert "P02, P01, P04, P09, P06" in trace
    assert "Optimal benefit: 550" in trace
    assert "Total route distance: 23 km" in trace
    assert "DP table" in trace
    assert "Warehouse: A:4, B:2, C:7" in trace


def main() -> None:
    tests = [
        test_sorting_priority_then_deadline,
        test_knapsack_sample_instance,
        test_knapsack_small_capacity,
        test_dijkstra_warehouse_paths,
        test_nearest_neighbor_route,
        test_end_to_end_trace,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"All {len(tests)} correctness checks passed.")


if __name__ == "__main__":
    main()
