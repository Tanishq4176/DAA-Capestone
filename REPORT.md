# Mini Courier Planner — Capstone Report

**Student:** Tanishq  
**Prototype:** sorting + 0/1 knapsack DP + Dijkstra + nearest-neighbor TSP

## Abstract

This project is an integrated courier-planning prototype. It reads parcel and road CSVs, ranks parcels, chooses a maximum-benefit subset that fits one vehicle, then builds a delivery tour that starts and ends at the warehouse. It also times the main algorithms on growing synthetic inputs and stores a runtime chart plus console traces. The design matches the five capstone phases: problem design, packing, routing, performance, and demonstration.

## 1. Problem and Design (Phase 1)

A courier receives parcels, each with destination, weight, declared value, deadline, and priority. One vehicle has a fixed weight capacity. The system must:

1. Order parcels so high priority and tight deadlines are visible.
2. Choose a subset that maximizes a transparent benefit score without exceeding capacity.
3. Route the chosen destinations over a weighted road network and return to the warehouse.

**Parcel attributes:** `parcel_id`, `destination`, `weight` (kg), `value`, `deadline` (smaller = more urgent), `priority` ∈ {High, Medium, Low}.

**Benefit score:** `value + 20 × priority_score + 5 × max(0, 6 − deadline)` with High/Medium/Low = 3/2/1. This is a planning proxy, not profit.

**Graph format:** undirected adjacency map from `datasets/routes.csv`. Each row is `source,destination,distance` with non-negative kilometres. The loader inserts both directions. Nodes are delivery points plus `Warehouse`.

**Why these algorithms**

| Need | Algorithm | Suitability |
|---|---|---|
| Rank by two keys, keep ties in input order | Python Timsort | Stable, O(n log n), appropriate for this n |
| Exact best subset under a weight limit | 0/1 knapsack DP | Weights are small integers; DP is exact |
| Shortest road distances, non-negative km | Dijkstra + binary heap | Correct for non-negative weights |
| Order several stops and return | Nearest-neighbor using Dijkstra distances | Fast TSP approximation; not globally optimal |

Flow: CSV validation → stable sort → 0/1 knapsack → Dijkstra shortest paths → nearest-neighbor tour → report.

```text
parcels.csv + routes.csv
        |                |
        v                v
   Timsort rank     adjacency graph
        |                |
        v                |
   0/1 knapsack          |
        |                |
        +-------> selected destinations
                         |
                         v
              Dijkstra + nearest neighbor
                         |
                         v
              packing plan + delivery route
```

## 2. Package Selection (Phase 2)

The small dataset has nine parcels and a 12 kg vehicle. Sorting uses `(-priority_score, deadline)`. Python’s `sorted` is Timsort and is stable, so P04 stays before P09 when both are High with deadline 3.

Knapsack recurrence:

`dp[i][c] = max(dp[i-1][c], benefit[i] + dp[i-1][c-weight[i]])` when the parcel fits; otherwise `dp[i][c] = dp[i-1][c]`.

The table is `(n+1) × (capacity+1)`. Time and space are O(nC). Reconstruction walks the table backward to recover the chosen IDs.

**Small-instance result (capacity 12):** selected `P02, P01, P04, P09, P06`, weight 12/12 kg, benefit 550. The full DP table is printed by `py app.py` and stored in `sample_output.txt`. A capacity-3 edge case selects a feasible subset with benefit 185.

## 3. Graph and Route (Phase 3)

The sample graph has 10 nodes (Warehouse, A–I) and 19 undirected roads. `images/road_graph.png` shows the layout.

Dijkstra from Warehouse on the selected stops:

- B: 2 km (`Warehouse -> B`)
- A: 3 km (`Warehouse -> B -> A`)
- D: 6 km (`Warehouse -> B -> D`)
- I: 9 km (`Warehouse -> B -> D -> I`)
- F: 8 km (`Warehouse -> B -> F`)

Nearest-neighbor stop order:

`Warehouse -> B -> A -> D -> F -> I -> Warehouse`

Total distance **23 km**. The program also expands each hop through the actual shortest-path nodes. Heap Dijkstra is O((V+E) log V). Repeated Dijkstra for k stops is about O(k(V+E) log V). The tour is a heuristic, not an exact TSP solver.

## 4. Performance Testing (Phase 4)

Two evidence layers:

1. **Real CSVs:** 9 parcels / 10 nodes (`datasets/parcels.csv`) and 30 parcels / 17 nodes (`datasets/parcels_large.csv`). Run the large case with capacity 25. Trace: `sample_output_large.txt`, screenshot: `images/console_demo_large.png`.
2. **Synthetic scaling:** `benchmark.py` builds deterministic parcel lists and ring-plus-chord graphs at sizes 10, 50, 100, and 200. Capacity is 12, 25, 50, and 100. Each algorithm is timed with `time.perf_counter` for five runs; the median is stored in `images/runtime_benchmarks.csv` and plotted in `images/runtime_benchmarks.png`.

Observed medians from one machine (milliseconds):

| Input size | Capacity | Sort | Knapsack | Dijkstra | Route |
|---:|---:|---:|---:|---:|---:|
| 10 | 12 | 0.0015 | 0.0146 | 0.0086 | 0.0815 |
| 50 | 25 | 0.0061 | 0.1404 | 0.0755 | 1.7294 |
| 100 | 50 | 0.0260 | 0.4821 | 0.1418 | 3.1458 |
| 200 | 100 | 0.0673 | 2.4628 | 0.2699 | 5.7993 |

These numbers are one Python/runtime/machine snapshot, not portable guarantees. Small timings include interpreter noise. Knapsack grows with both n and C. Route cost grows with graph size and stop count, and dominates the other steps.

**Optimization ideas**

- 1D knapsack storage when the subset can be reconstructed separately.
- Cache Dijkstra trees or precompute a k×k distance matrix on selected stops.
- Two-opt improvement on the nearest-neighbor tour.
- More repeats and more machines for a stabler benchmark.

Correctness of the small instance is locked by `py tests/test_correctness.py` (sort order, DP optimum 550, Dijkstra paths, 23 km tour).

## 5. Results and Demonstration (Phase 5)

Run `py app.py` for the 12 kg sample. The console screenshot is `images/console_demo.png`. The same text is `sample_output.txt`.

The prototype:

- Validates unique IDs, fields, graph nodes, non-negative distances, capacity, and reachability.
- Shows the adjacency list, ranked parcels, DP table, packing plan, shortest paths, stop order, expanded road path, and total km.
- Is a teaching demo, not a production dispatcher: one vehicle, no time windows, scalar benefit, heuristic tour.

## Conclusion and future scope

The project joins Timsort, 0/1 knapsack, Dijkstra, and a TSP approximation in one reproducible workflow. Packing is exact for the chosen score and capacity. Routing is practical and approximate. Future work: time windows, travel times, exact TSP on tiny stop sets, multi-vehicle models, and larger real maps.
