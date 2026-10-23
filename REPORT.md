# Mini Courier Planner — Capstone Report

## Abstract

This project combines parcel prioritization, capacity constrained package selection, shortest path computation, and approximate delivery routing. The runnable prototype reads CSV inputs, selects a maximum benefit parcel subset for one vehicle trip, and produces a route that starts and ends at the warehouse. It also benchmarks the main algorithmic components and saves a runtime chart and sample console trace.

## 1. Problem and Design (Phase 1)

A courier has parcels with destination, weight, declared value, deadline, and priority. The vehicle has a fixed weight capacity. The system must choose parcels that maximize a transparent benefit score, then route among their destinations over a weighted road network.

The parcel benefit is `value + 20 × priority_score + 5 × max(0, 6 − deadline)`, where High, Medium, Low map to 3, 2, 1. This score is a planning proxy, not monetary profit. The graph is an undirected adjacency map loaded from `datasets/routes.csv`; edge weights are non-negative kilometres. Sorting is stable by priority descending and deadline ascending. The DP knapsack chooses the optimal parcel subset for the defined score and weight capacity. Dijkstra computes road shortest paths. Nearest neighbor is a heuristic for ordering stops, and does not guarantee a globally shortest tour.

Flow: CSV validation → stable parcel sort → 0/1 knapsack → shortest paths → nearest-neighbor tour → report output.

## 2. Package Selection (Phase 2)

The supplied dataset contains nine parcels and a 12 kg vehicle. The benefit score is optimized exactly by 0/1 knapsack. The dynamic programming recurrence is:

`dp[i][c] = max(dp[i-1][c], benefit[i] + dp[i-1][c-weight[i]])` when the parcel fits; otherwise `dp[i][c] = dp[i-1][c]`.

The retained table is `(n+1) × (capacity+1)`. Time and space are O(nC), with C the integer capacity. Sorting costs O(n log n) in the comparison model. The output trace in `sample_output.txt` records the selected IDs, weight, score, and table dimensions.

## 3. Graph and Route (Phase 3)

The road CSV stores one undirected edge per row; the loader inserts both directions. Dijkstra's heap implementation has O((V+E) log V) time and O(V+E) graph storage. It requires non-negative edge weights. Each selected destination is shown with the shortest path from Warehouse. The route planner repeatedly chooses the closest remaining selected destination using shortest-path distance, then returns to Warehouse. Its straightforward implementation runs Dijkstra for each stop, approximately O(k(V+E) log V), for k stops.

## 4. Performance Testing (Phase 4)

`benchmark.py` creates deterministic synthetic parcel lists and connected ring-plus-chord road graphs at sizes 10, 50, 100, and 200. Capacity is 12, 25, 50, and 100 respectively. Each algorithm is timed with `time.perf_counter` for five repetitions; the median is recorded in `images/runtime_benchmarks.csv` and plotted in `images/runtime_benchmarks.png`.

| Input size | Capacity | Sort (ms) | Knapsack (ms) | Dijkstra (ms) | Route (ms) |
|---:|---:|---:|---:|---:|---:|
| 10 | 12 | 0.0015 | 0.0166 | 0.0088 | 0.1616 |
| 50 | 25 | 0.0130 | 0.1311 | 0.0385 | 1.2776 |
| 100 | 50 | 0.0121 | 0.5397 | 0.1280 | 2.3383 |
| 200 | 100 | 0.0267 | 1.9776 | 0.1501 | 4.8662 |

These are illustrative measurements from one Python/runtime/machine execution, not portable guarantees. Small timings are affected by interpreter and operating-system noise. Knapsack scales with both n and C; in this experiment both increase. Route cost grows with graph size and number of delivery stops. For larger workloads, possible improvements include 1D DP storage when reconstruction is handled separately, caching Dijkstra results / using a precomputed selected-stop distance matrix, reducing the number of route candidates, and benchmarking across more repetitions and machines.

## 5. Results and Demonstration (Phase 5)

Run `py app.py` to reproduce the sample planning trace or `py app.py --capacity 15` for another capacity. The sample trace is saved as `sample_output.txt`. Run `py benchmark.py` to regenerate benchmark data and the chart. The main notebook, `mini_courier_planner.ipynb`, documents phases 1–5 and invokes the modular implementation.

The prototype validates parcel fields, unique IDs, graph nodes, edge weights, capacity, and route reachability. It is a demonstration, not a production dispatch system: it optimizes the declared scalar benefit, has no time windows or vehicle fleet model, and uses a heuristic route order.

## Conclusion and Future Scope

The project joins sorting, dynamic programming, Dijkstra, and a TSP approximation in one reproducible workflow. It gives an exact optimum for parcel benefit under the chosen capacity model and practical, approximate routing over the supplied graph. Future work could model time windows and service times, use road travel times, compare against exact TSP on small instances, add multi-vehicle planning, and evaluate larger real-world networks.
