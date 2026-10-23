"""Dijkstra shortest-path helpers for the Mini Courier Planner."""

from heapq import heappop, heappush


def dijkstra(graph, start):
    """Return shortest distances and previous-node links from start."""
    if start not in graph:
        raise ValueError(f"Start node {start!r} is not present in the graph")
    if any(weight < 0 for edges in graph.values() for weight in edges.values()):
        raise ValueError("Dijkstra's algorithm requires non-negative edge weights")
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, edge_weight in graph[current_node].items():
            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def shortest_path(previous, destination):
    """Reconstruct a shortest path from a previous-node map."""
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous.get(current)

    return list(reversed(path))

