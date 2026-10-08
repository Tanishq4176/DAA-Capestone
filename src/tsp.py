"""Nearest-neighbor route planning for the Mini Courier Planner."""

from src.dijkstra import dijkstra


def plan_nearest_neighbor_route(graph, start, destinations):
    """Build a practical route through destinations and back to start."""
    route = [start]
    total_distance = 0
    current = start
    unvisited = set(destinations)

    while unvisited:
        distances, _ = dijkstra(graph, current)
        next_destination = min(
            unvisited,
            key=lambda destination: distances[destination],
        )
        total_distance += distances[next_destination]
        route.append(next_destination)
        current = next_destination
        unvisited.remove(next_destination)

    distances, _ = dijkstra(graph, current)
    total_distance += distances[start]
    route.append(start)

    return route, total_distance

