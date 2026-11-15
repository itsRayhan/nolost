from django.test import TestCase, Client
from .algorithms import a_star, dijkstra, bfs, dfs


class PathfindingTests(TestCase):
    def test_a_star_default_route(self):
        res = a_star("A", "J")
        self.assertTrue(res["found"])
        self.assertEqual(res["path"], ["A", "B", "D", "G", "J"])

    def test_dijkstra_matches_a_star_distance(self):
        res_a = a_star("A", "J")
        res_d = dijkstra("A", "J")
        self.assertEqual(res_a["distance_km"], res_d["distance_km"])

    def test_bfs_and_dfs_find_valid_paths(self):
        for algo in (bfs, dfs):
            res = algo("A", "J")
            self.assertTrue(res["found"])
            self.assertEqual(res["path"][0], "A")
            self.assertEqual(res["path"][-1], "J")

    def test_api_endpoint(self):
        client = Client()
        response = client.get("/api/find-path/", {"source": "A", "destination": "J", "algorithm": "A*"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["selected"]["path"], ["A", "B", "D", "G", "J"])
        self.assertEqual(len(data["comparison"]), 4)
