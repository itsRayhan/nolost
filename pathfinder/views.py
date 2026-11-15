import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .algorithms import run_pathfinding
from .graph_data import NODES, get_edge_list


def index(request):
    """Render the main Nolost maps pathfinding visualizer page."""
    nodes_list = list(NODES.values())
    edges_list = get_edge_list()

    # Precompute default path (Node A -> Node J using A*) so the map renders immediately
    default_result = run_pathfinding("A", "J", "A*")

    context = {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "nodes": nodes_list,
        "nodes_json": json.dumps(nodes_list),
        "edges_json": json.dumps(edges_list),
        "default_result_json": json.dumps(default_result),
    }
    return render(request, "pathfinder/index.html", context)


@require_GET
def find_path_api(request):
    """API endpoint returning computed route and performance metrics across all algorithms."""
    source = request.GET.get("source", "A").strip().upper()
    destination = request.GET.get("destination", "J").strip().upper()
    algorithm = request.GET.get("algorithm", "A*").strip()

    if source not in NODES or destination not in NODES:
        return JsonResponse(
            {"error": "Invalid source or destination node selected."},
            status=400,
        )

    result = run_pathfinding(source, destination, algorithm)
    return JsonResponse(result)
