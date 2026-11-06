"""Nearest-neighbor route planning for the Mini Courier Planner."""

from src.dijkstra import dijkstra, shortest_path


def plan_nearest_neighbor_route(graph, start, destinations):
    """Build a practical route through destinations and back to start."""
    unknown = set(destinations) - set(graph)
    if start not in graph or unknown:
        raise ValueError(f"Unknown route nodes: {sorted(unknown)}")
    if any(weight < 0 for edges in graph.values() for weight in edges.values()):
        raise ValueError("Dijkstra's algorithm requires non-negative edge weights")
    route = [start]
    total_distance = 0
    current = start
    unvisited = list(dict.fromkeys(destinations))
    if start in unvisited:
        unvisited.remove(start)

    while unvisited:
        distances, _ = dijkstra(graph, current)
        next_destination = min(unvisited, key=lambda destination: distances[destination])
        if distances[next_destination] == float("inf"):
            raise ValueError(f"Destination {next_destination!r} is unreachable from {current!r}")
        total_distance += distances[next_destination]
        route.append(next_destination)
        current = next_destination
        unvisited.remove(next_destination)

    distances, _ = dijkstra(graph, current)
    if distances[start] == float("inf"):
        raise ValueError(f"Warehouse {start!r} is unreachable from {current!r}")
    total_distance += distances[start]
    route.append(start)

    return route, total_distance


def expand_route_with_shortest_paths(graph, stop_sequence):
    """Insert Dijkstra shortest-path hops between consecutive delivery stops."""
    if not stop_sequence:
        return []
    expanded = [stop_sequence[0]]
    for origin, destination in zip(stop_sequence, stop_sequence[1:]):
        _, previous = dijkstra(graph, origin)
        hop = shortest_path(previous, destination)
        if not hop or hop[0] != origin:
            raise ValueError(f"No reconstructed path from {origin!r} to {destination!r}")
        expanded.extend(hop[1:])
    return expanded

