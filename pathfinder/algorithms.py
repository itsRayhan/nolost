"""
Pathfinding algorithm implementations (BFS, DFS, Dijkstra, A*)
with performance metrics tracking (distance, hops, nodes visited, execution time).
"""

import heapq
import time
from collections import deque
from .graph_data import GRAPH, NODES, haversine_distance


def _compute_path_distance(path: list) -> float:
    """Sum edge weights along a given node path."""
    if not path or len(path) < 2:
        return 0.0
    total = 0.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        for neighbor, weight in GRAPH[u]:
            if neighbor == v:
                total += weight
                break
    return round(total, 3)


def bfs(start: str, goal: str) -> dict:
    """Breadth-First Search: guarantees fewest hops/edges, unweighted."""
    t0 = time.perf_counter()
    queue = deque([[start]])
    visited = {start}
    nodes_explored = 0

    while queue:
        path = queue.popleft()
        current = path[-1]
        nodes_explored += 1

        if current == goal:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
            return {
                "algorithm": "BFS",
                "full_name": "Breadth-First Search",
                "found": True,
                "path": path,
                "distance_km": _compute_path_distance(path),
                "hops": len(path) - 1,
                "nodes_explored": nodes_explored,
                "execution_time_ms": elapsed_ms,
            }

        for neighbor, _ in GRAPH[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
    return {
        "algorithm": "BFS",
        "full_name": "Breadth-First Search",
        "found": False,
        "path": [],
        "distance_km": 0.0,
        "hops": 0,
        "nodes_explored": nodes_explored,
        "execution_time_ms": elapsed_ms,
    }


def dfs(start: str, goal: str) -> dict:
    """Depth-First Search: explores deep branches first, non-optimal."""
    t0 = time.perf_counter()
    stack = [[start]]
    visited = set()
    nodes_explored = 0

    while stack:
        path = stack.pop()
        current = path[-1]

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        if current == goal:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
            return {
                "algorithm": "DFS",
                "full_name": "Depth-First Search",
                "found": True,
                "path": path,
                "distance_km": _compute_path_distance(path),
                "hops": len(path) - 1,
                "nodes_explored": nodes_explored,
                "execution_time_ms": elapsed_ms,
            }

        # Push neighbors in reverse alphabetical order so 'A'..'Z' pops first
        for neighbor, _ in reversed(GRAPH[current]):
            if neighbor not in visited:
                stack.append(path + [neighbor])

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
    return {
        "algorithm": "DFS",
        "full_name": "Depth-First Search",
        "found": False,
        "path": [],
        "distance_km": 0.0,
        "hops": 0,
        "nodes_explored": nodes_explored,
        "execution_time_ms": elapsed_ms,
    }


def dijkstra(start: str, goal: str) -> dict:
    """Dijkstra's Algorithm: guarantees shortest weighted distance."""
    t0 = time.perf_counter()
    pq = [(0.0, start, [start])]
    best_dist = {node: float("inf") for node in NODES}
    best_dist[start] = 0.0
    visited = set()
    nodes_explored = 0

    while pq:
        cost, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        if current == goal:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
            return {
                "algorithm": "Dijkstra",
                "full_name": "Dijkstra's Shortest Path",
                "found": True,
                "path": path,
                "distance_km": round(cost, 3),
                "hops": len(path) - 1,
                "nodes_explored": nodes_explored,
                "execution_time_ms": elapsed_ms,
            }

        for neighbor, weight in GRAPH[current]:
            if neighbor not in visited:
                new_cost = cost + weight
                if new_cost < best_dist[neighbor]:
                    best_dist[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
    return {
        "algorithm": "Dijkstra",
        "full_name": "Dijkstra's Shortest Path",
        "found": False,
        "path": [],
        "distance_km": 0.0,
        "hops": 0,
        "nodes_explored": nodes_explored,
        "execution_time_ms": elapsed_ms,
    }


def a_star(start: str, goal: str) -> dict:
    """A* Search Algorithm: uses Haversine straight-line heuristic for fast optimal routing."""
    t0 = time.perf_counter()
    h0 = haversine_distance(start, goal)
    # Priority queue tuple: (f_score, g_score, current_node, path)
    pq = [(h0, 0.0, start, [start])]
    g_scores = {node: float("inf") for node in NODES}
    g_scores[start] = 0.0
    visited = set()
    nodes_explored = 0

    while pq:
        f_score, g_score, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        if current == goal:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
            return {
                "algorithm": "A*",
                "full_name": "A* Search (Haversine Heuristic)",
                "found": True,
                "path": path,
                "distance_km": round(g_score, 3),
                "hops": len(path) - 1,
                "nodes_explored": nodes_explored,
                "execution_time_ms": elapsed_ms,
            }

        for neighbor, weight in GRAPH[current]:
            if neighbor not in visited:
                tentative_g = g_score + weight
                if tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    f_new = tentative_g + haversine_distance(neighbor, goal)
                    heapq.heappush(pq, (f_new, tentative_g, neighbor, path + [neighbor]))

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 4)
    return {
        "algorithm": "A*",
        "full_name": "A* Search (Haversine Heuristic)",
        "found": False,
        "path": [],
        "distance_km": 0.0,
        "hops": 0,
        "nodes_explored": nodes_explored,
        "execution_time_ms": elapsed_ms,
    }


ALGORITHM_REGISTRY = {
    "A*": a_star,
    "Dijkstra": dijkstra,
    "BFS": bfs,
    "DFS": dfs,
}


def run_pathfinding(start: str, goal: str, selected_algorithm: str) -> dict:
    """
    Execute the requested pathfinding algorithm and also run all 4 algorithms
    to produce a complete side-by-side performance comparison.
    """
    if selected_algorithm not in ALGORITHM_REGISTRY:
        selected_algorithm = "A*"

    selected_result = ALGORITHM_REGISTRY[selected_algorithm](start, goal)
    selected_result["coordinates"] = [
        {
            "id": nid,
            "label": NODES[nid]["label"],
            "landmark": NODES[nid]["landmark"],
            "lat": NODES[nid]["lat"],
            "lng": NODES[nid]["lng"],
        }
        for nid in selected_result["path"]
    ]

    comparison = []
    for algo_key in ["A*", "Dijkstra", "BFS", "DFS"]:
        res = ALGORITHM_REGISTRY[algo_key](start, goal)
        comparison.append(res)

    return {
        "selected": selected_result,
        "comparison": comparison,
    }
