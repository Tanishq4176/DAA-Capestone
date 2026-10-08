# Mini-Courier Planner

This project is a DAA capstone prototype for a courier company. It plans one delivery trip by modelling parcels, choosing the best parcels for the vehicle capacity, and building a practical delivery route.

The complete combined implementation is in `mini_courier_planner.ipynb`.

The assignment is also separated into different notebooks:

| Notebook | Contents |
|---|---|
| `01_phase1_problem_design.ipynb` | Question 1 / Phase 1: problem design and planning |
| `02_phase2_package_selection.ipynb` | Question 2 / Phase 2: package prioritization and box filling |
| `03_phase3_route_planning.ipynb` | Question 3 / Phase 3: shortest path and route planning |

## Phase 1: Problem Design

Phase 1 defines the courier-planning problem and prepares the data model.

A courier company receives many parcels, but the delivery vehicle has limited capacity. Each parcel has a destination, weight, value, deadline, and priority. The system must decide which parcels should be loaded and later decide how to deliver them efficiently.

Parcel attributes used in the notebook:

| Attribute | Meaning |
|---|---|
| `parcel_id` | Unique parcel identifier |
| `destination` | Delivery location code |
| `weight` | Capacity used by the parcel |
| `value` | Business reward or delivery value |
| `deadline` | Delivery urgency; smaller value means earlier deadline |
| `priority` | High, Medium, or Low priority |
| `benefit` | Combined score used by optimization |

The road network is planned as a weighted graph:

| Graph Element | Courier Meaning |
|---|---|
| Node | Warehouse or delivery location |
| Edge | Road between two locations |
| Edge weight | Distance or travel time |

## Phase 2: Package Prioritization and Box Filling

Phase 2 sorts parcels and selects the best parcel set for one delivery trip.

### Sorting Theory

Parcels are sorted by:

1. Higher priority first.
2. Earlier deadline first.

This gives urgent and important parcels first consideration. Python's sorting is stable, so if two parcels have the same priority and deadline, their original order is preserved.

### Dynamic Programming Theory

The box-filling problem is treated as a 0/1 knapsack problem:

- Each parcel can either be selected or not selected.
- Parcel weight is the cost.
- Parcel benefit is the value to maximize.
- Vehicle capacity is the maximum allowed weight.

The recurrence used is:

```text
dp[i][w] = max(dp[i - 1][w], benefit[i - 1] + dp[i - 1][w - weight[i - 1]])
```

Where:

- `i` is the number of parcels considered.
- `w` is the current capacity.
- `dp[i][w]` stores the best benefit possible.

Time complexity: `O(n * capacity)`

Space complexity: `O(n * capacity)`

### Phase 2 Summary

The notebook uses sample parcel data and a vehicle capacity of 12 kg. It calculates a benefit score using parcel value, priority bonus, and urgency bonus. The dynamic programming table then selects the parcel combination with the maximum total benefit while staying within capacity.

Test cases verify:

- Selected parcels do not exceed vehicle capacity.
- A small-capacity edge case works.
- Stable sorting keeps equal-priority parcels in input order.

## Phase 3: Shortest Path and Route Planning

Phase 3 turns the selected parcel destinations into a graph-based route-planning problem.

### Dijkstra's Algorithm Theory

Dijkstra's algorithm finds the shortest distance from one source node to all other nodes in a graph with non-negative edge weights.

In this project:

- The source is the warehouse or the current courier location.
- Nodes are delivery points.
- Edge weights represent distance.
- The algorithm returns shortest distances and previous-node links for path reconstruction.

With a priority queue, the time complexity is approximately:

```text
O((V + E) log V)
```

Where:

- `V` is the number of vertices.
- `E` is the number of edges.

### Nearest-Neighbor Route Theory

After the best parcels are selected, the system must order their destinations. The notebook uses the nearest-neighbor heuristic:

1. Start from the warehouse.
2. Find the closest unvisited selected destination using Dijkstra's algorithm.
3. Move to that destination.
4. Repeat until all selected destinations are visited.
5. Return to the warehouse.

This is a heuristic for the travelling-salesman-style route problem. It is fast and easy to implement, but it does not always produce the globally optimal route.

### Phase 3 Summary

The notebook defines a sample road graph containing the warehouse and locations `A` to `I`. It computes shortest paths from the warehouse to selected delivery destinations and then builds an approximate complete route using nearest neighbor.

## Overall Summary

The project now completes the first three phases:

| Phase | Work Completed |
|---|---|
| Phase 1 | Problem definition, parcel model, graph model, and algorithm plan |
| Phase 2 | Parcel sorting and 0/1 knapsack-based parcel selection |
| Phase 3 | Dijkstra shortest paths and nearest-neighbor route planning |

Together, these phases form a working mini courier planner:

1. Understand and structure the courier data.
2. Select the most beneficial parcels under vehicle capacity.
3. Generate a practical delivery route for the selected destinations.

## How to Use

Open any notebook in Jupyter Notebook, JupyterLab, or VS Code and run the cells from top to bottom. The separated notebooks are self-contained, so each one can be run independently.
