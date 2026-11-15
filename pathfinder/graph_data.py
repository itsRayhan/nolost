"""
Manual graph representation (12 nodes in Dhaka, Bangladesh) with real GPS coordinates
and weighted edges computed using Haversine distance (in kilometers).
"""

import math

# 12 manually defined nodes (satisfying the 10-20 nodes requirement)
# Positioned across central Dhaka matching the map layout.
NODES = {
    "A": {
        "id": "A",
        "label": "Node A",
        "landmark": "Shahbagh",
        "lat": 23.7389,
        "lng": 90.3958,
    },
    "B": {
        "id": "B",
        "label": "Node B",
        "landmark": "Banglamotor",
        "lat": 23.7465,
        "lng": 90.3982,
    },
    "C": {
        "id": "C",
        "label": "Node C",
        "landmark": "Kakrail",
        "lat": 23.7335,
        "lng": 90.4055,
    },
    "D": {
        "id": "D",
        "label": "Node D",
        "landmark": "Moghbazar",
        "lat": 23.7495,
        "lng": 90.4095,
    },
    "E": {
        "id": "E",
        "label": "Node E",
        "landmark": "Tejgaon",
        "lat": 23.7580,
        "lng": 90.4005,
    },
    "F": {
        "id": "F",
        "label": "Node F",
        "landmark": "Motijheel",
        "lat": 23.7285,
        "lng": 90.4140,
    },
    "G": {
        "id": "G",
        "label": "Node G",
        "landmark": "Malibagh",
        "lat": 23.7435,
        "lng": 90.4185,
    },
    "H": {
        "id": "H",
        "label": "Node H",
        "landmark": "Rampura",
        "lat": 23.7625,
        "lng": 90.4168,
    },
    "I": {
        "id": "I",
        "label": "Node I",
        "landmark": "Bashabo",
        "lat": 23.7330,
        "lng": 90.4275,
    },
    "J": {
        "id": "J",
        "label": "Node J",
        "landmark": "Meradia",
        "lat": 23.7535,
        "lng": 90.4290,
    },
    "K": {
        "id": "K",
        "label": "Node K",
        "landmark": "Karwan Bazar",
        "lat": 23.7512,
        "lng": 90.3930,
    },
    "L": {
        "id": "L",
        "label": "Node L",
        "landmark": "Farmgate",
        "lat": 23.7572,
        "lng": 90.3885,
    },
}

# Undirected graph edges (connections between adjacent intersections/nodes)
RAW_EDGES = [
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("B", "E"),
    ("B", "K"),
    ("C", "F"),
    ("D", "E"),
    ("D", "G"),
    ("D", "H"),
    ("E", "H"),
    ("E", "K"),
    ("E", "L"),
    ("F", "G"),
    ("F", "I"),
    ("G", "I"),
    ("G", "J"),
    ("H", "J"),
    ("I", "J"),
    ("K", "L"),
]


def haversine_distance(node_id_1: str, node_id_2: str) -> float:
    """
    Calculate the great-circle distance in kilometers between two nodes
    on Earth using the Haversine formula.
    """
    n1 = NODES[node_id_1]
    n2 = NODES[node_id_2]

    r = 6371.0  # Earth radius in kilometers
    lat1, lon1 = math.radians(n1["lat"]), math.radians(n1["lng"])
    lat2, lon2 = math.radians(n2["lat"]), math.radians(n2["lng"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 3)


def build_adjacency_list() -> dict:
    """
    Construct weighted undirected adjacency list:
    { 'A': [('B', 0.88), ('C', 1.16)], ... }
    """
    graph = {node_id: [] for node_id in NODES}
    for u, v in RAW_EDGES:
        dist = haversine_distance(u, v)
        graph[u].append((v, dist))
        graph[v].append((u, dist))

    # Sort neighbors alphabetically for deterministic BFS/DFS traversal
    for node_id in graph:
        graph[node_id].sort(key=lambda item: item[0])

    return graph


GRAPH = build_adjacency_list()


def get_edge_list() -> list:
    """Return all unique edges with coordinates and distance for map rendering."""
    edges = []
    for u, v in RAW_EDGES:
        edges.append(
            {
                "from": u,
                "to": v,
                "distance": haversine_distance(u, v),
                "from_coords": {"lat": NODES[u]["lat"], "lng": NODES[u]["lng"]},
                "to_coords": {"lat": NODES[v]["lat"], "lng": NODES[v]["lng"]},
            }
        )
    return edges
