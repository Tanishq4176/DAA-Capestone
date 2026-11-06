# Mini Courier Planner

**Student:** Tanishq  
Capstone prototype for an intelligent courier planner: parcel prioritization, capacity-constrained packing, shortest paths, approximate routing, and runtime comparison.

Given a list of parcels and a road network, the program prints an ordered delivery route and an optimized packing plan. It combines sorting, 0/1 knapsack dynamic programming, Dijkstra’s algorithm, and a nearest-neighbor TSP approximation.

## Assignment coverage

| Phase | Task | Where to look |
|---|---|---|
| 1 | Problem design, parcel attributes, graph format, algorithm plan | `01_phase1_problem_design.ipynb`, `REPORT.md` §1 |
| 2 | Sort by priority/deadline, 0/1 knapsack packing | `src/sorting.py`, `src/knapsack.py`, `02_phase2_package_selection.ipynb` |
| 3 | Customer graph, Dijkstra, nearest-neighbor route | `src/dijkstra.py`, `src/tsp.py`, `03_phase3_route_planning.ipynb` |
| 4 | Small and larger data, runtimes, optimization notes | `benchmark.py`, `datasets/parcels_large.csv`, `REPORT.md` §4 |
| 5 | Working demo, traces, screenshots, documentation | `app.py`, `sample_output.txt`, `images/`, this README |

## Setup and execution

Requires Python 3.10 or later.

```powershell
py -m pip install -r requirements.txt
py tests/test_correctness.py
py app.py
py app.py --capacity 15
py app.py --capacity 25 --parcels datasets/parcels_large.csv --routes datasets/routes_large.csv
py benchmark.py
```

Open the phase notebooks or `mini_courier_planner.ipynb` in Jupyter or VS Code. `REPORT.md` is the written report.

## Sample data

- `datasets/parcels.csv`: 9-parcel lab instance (ID, destination, weight kg, value, deadline, priority).
- `datasets/routes.csv`: undirected weighted roads; distance is non-negative km.
- `datasets/parcels_large.csv` and `datasets/routes_large.csv`: larger demonstration instance (30 parcels, 17 nodes).

Parcel benefit is `value + 20 × priority_score + 5 × max(0, 6 − deadline)`, with High/Medium/Low = 3/2/1. The score is a planning proxy, not money.

## Project structure

```text
app.py                              Integrated command-line application
benchmark.py                        Scalability benchmark + evidence images
REPORT.md                           Capstone report
sample_output.txt                   Small-instance console trace
sample_output_large.txt             Larger-instance console trace
tests/test_correctness.py           Sorting, DP, Dijkstra, and route checks
01_phase1_problem_design.ipynb      Phase 1 design
02_phase2_package_selection.ipynb   Phase 2 selection
03_phase3_route_planning.ipynb      Phase 3 graph planning
04_phase4_performance.ipynb         Phase 4 timing and optimization
05_phase5_demonstration.ipynb       Phase 5 demonstration
mini_courier_planner.ipynb          Integrated phases 1–5 notebook
src/                                Reusable algorithms
datasets/                           Parcel and road CSV files
images/                             Charts, graph figure, console screenshots
```

## Evidence artifacts

| Rubric item | Artifact |
|---|---|
| Sorted parcels and packing plan | `sample_output.txt`, `images/console_demo.png` |
| DP table | `images/dp_table.png`, printed in `app.py` output |
| Graph + shortest paths + route length | `images/road_graph.png`, console trace |
| Runtime chart and larger dataset | `images/runtime_benchmarks.png`, `images/console_demo_large.png` |
| Correctness | `py tests/test_correctness.py` |

## Complexity

| Component | Time | Space |
|---|---:|---:|
| Timsort | O(n log n) | O(n) |
| 0/1 knapsack | O(nC) | O(nC) reconstruction table |
| Dijkstra with heap | O((V+E) log V) | O(V+E) |
| Nearest neighbor with repeated Dijkstra | O(k(V+E) log V) | O(V+E) |

n = parcels, C = capacity, V/E = graph size, k = delivery stops. The route heuristic is not a guaranteed optimal TSP tour.
