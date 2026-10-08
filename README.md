# Mini Courier Planner

A Design and Analysis of Algorithms (DAA) capstone project completed through
Phase 3. The project plans one courier trip by modelling parcels, selecting the
best parcels for a limited-capacity vehicle, and building a practical delivery
route.

## Project Overview

The Mini Courier Planner solves three connected courier-planning tasks:

1. Define parcel and road-network data for a courier company.
2. Prioritize parcels and select the best parcel set under vehicle capacity.
3. Compute shortest delivery paths and create a delivery route.

The implementation is available as notebooks for assignment presentation and as
small reusable Python modules in `src/`.

## Algorithms Used

| Phase | Algorithm | Purpose |
|---|---|---|
| Phase 1 | Data modelling | Represent parcels and delivery locations |
| Phase 2 | Stable sorting | Prioritize parcels by priority and deadline |
| Phase 2 | 0/1 knapsack dynamic programming | Select parcels within vehicle capacity |
| Phase 3 | Dijkstra's algorithm | Find shortest paths in the road graph |
| Phase 3 | Nearest-neighbor route planning | Build a practical delivery tour |

## Project Structure

```text
Mini-Courier-Planner/
|-- datasets/
|   |-- parcels.csv                 # Sample parcel dataset
|   `-- routes.csv                  # Sample weighted road network
|-- src/
|   |-- __init__.py
|   |-- sorting.py                  # Parcel priority and benefit helpers
|   |-- knapsack.py                 # 0/1 knapsack parcel selection
|   |-- dijkstra.py                 # Shortest-path calculation
|   `-- tsp.py                      # Nearest-neighbor route planning
|-- 01_phase1_problem_design.ipynb
|-- 02_phase2_package_selection.ipynb
|-- 03_phase3_route_planning.ipynb
|-- mini_courier_planner.ipynb      # Combined Phase 1-3 notebook
|-- requirements.txt
`-- README.md
```

## Phase 1: Problem Design

Phase 1 defines the courier-planning problem and prepares the data model.

Each parcel has:

| Attribute | Meaning |
|---|---|
| `parcel_id` | Unique parcel identifier |
| `destination` | Delivery location code |
| `weight` | Vehicle capacity used by the parcel |
| `value` | Business reward or delivery value |
| `deadline` | Delivery urgency; smaller means earlier |
| `priority` | High, Medium, or Low priority |

The road network is represented as a weighted graph:

| Graph Element | Courier Meaning |
|---|---|
| Node | Warehouse or delivery location |
| Edge | Road between two locations |
| Edge weight | Distance or travel time |

## Phase 2: Package Prioritization and Box Filling

Parcels are sorted by higher priority first and earlier deadline second. Python's
stable sorting keeps the original order for parcels with equal priority and
deadline.

The parcel-selection problem is solved as a 0/1 knapsack problem:

```text
dp[i][w] = max(dp[i - 1][w], benefit[i - 1] + dp[i - 1][w - weight[i - 1]])
```

Where:

- `i` is the number of parcels considered.
- `w` is the current vehicle capacity.
- `dp[i][w]` stores the best benefit possible.

Time complexity: `O(n * capacity)`

Space complexity: `O(n * capacity)`

## Phase 3: Shortest Path and Route Planning

Dijkstra's algorithm calculates shortest distances from the warehouse or current
delivery point to every other point in the road network.

After parcel selection, the nearest-neighbor route planner:

1. Starts from the warehouse.
2. Chooses the closest unvisited selected destination.
3. Moves to that destination.
4. Repeats until all selected destinations are visited.
5. Returns to the warehouse.

This is a fast heuristic for delivery-route planning. It gives a practical route
but does not guarantee a globally optimal travelling-salesman solution.

## Outputs Through Phase 3

The project produces:

- Prioritized parcels.
- Selected parcels that fit within vehicle capacity.
- Shortest paths from the warehouse to selected destinations.
- A nearest-neighbor delivery route that starts and ends at the warehouse.
- The approximate total route distance.

Performance benchmarking, runtime charts, and generated image outputs are not
included because this version intentionally stops at Phase 3.

## How to Run

Install the notebook dependency:

```powershell
py -m pip install -r requirements.txt
```

Open the notebooks in Jupyter Notebook, JupyterLab, or VS Code and run cells from
top to bottom:

```powershell
py -m jupyter notebook
```

Use `mini_courier_planner.ipynb` for the complete Phase 1-3 flow, or run the
separate phase notebooks independently.
