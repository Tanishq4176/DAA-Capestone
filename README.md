# Mini Courier Planner

A modular capstone prototype for parcel prioritization, capacity constrained packing, shortest paths, approximate route planning, and runtime comparison. The implementation covers all five assignment phases.

## Features

- Stable parcel ordering by priority (High → Low), then earliest deadline.
- 0/1 knapsack dynamic programming to maximize a defined parcel benefit within vehicle capacity.
- CSV-backed undirected weighted road network and Dijkstra shortest paths.
- Nearest-neighbor route through selected destinations, returning to the warehouse.
- Repeatable synthetic benchmark with median runtime CSV and chart.
- Input validation and a reproducible sample output trace.

## Setup and execution

Requires Python 3.10 or later.

```powershell
py -m pip install -r requirements.txt
py app.py
py app.py --capacity 15
py benchmark.py
```

Open `mini_courier_planner.ipynb` in Jupyter or VS Code for the end-to-end notebook presentation. `REPORT.md` contains the design, complexity analysis, benchmark method, observations, and future scope.

## Sample data

- `datasets/parcels.csv`: parcel ID, destination, weight (kg), value, deadline, priority.
- `datasets/routes.csv`: one undirected road edge per row; distance is non-negative km.

The parcel score is `value + 20 × priority_score + 5 × max(0, 6 − deadline)`, where High/Medium/Low scores are 3/2/1. The score is an explicit prototype assumption, not a currency amount.

## Project structure

```text
app.py                         Integrated command-line application
benchmark.py                   Synthetic scalability benchmark
REPORT.md                      Final capstone report
sample_output.txt              Reproducible console output trace
01_phase1_problem_design.ipynb Phase 1 design
02_phase2_package_selection.ipynb Phase 2 selection
03_phase3_route_planning.ipynb  Phase 3 graph planning
mini_courier_planner.ipynb      Integrated phases 1–5 notebook
src/                            Reusable algorithms
datasets/                       Parcel and road CSV files
images/                          Runtime chart and benchmark CSV
```

## Complexity

| Component | Time | Space |
|---|---:|---:|
| Sorting | O(n log n) | O(n) |
| 0/1 knapsack | O(nC) | O(nC) with retained reconstruction table |
| Dijkstra with heap | O((V+E) log V) | O(V+E) |
| Nearest neighbor with repeated Dijkstra | O(k(V+E) log V) | O(V+E) |

Here n is parcel count, C vehicle capacity, V/E graph nodes/edges, and k selected delivery stops. The route heuristic is not guaranteed to find the optimal TSP tour.

## Benchmark and artifacts

`py benchmark.py` benchmarks sizes 10, 50, 100, and 200, repeats each measurement five times, and writes median timings to `images/runtime_benchmarks.csv` and `images/runtime_benchmarks.png`. Results vary by machine; see `REPORT.md` for the observed data and limitations. `sample_output.txt` demonstrates the application output.
