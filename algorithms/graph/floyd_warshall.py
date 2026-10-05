from typing import Any, Dict, List, Tuple
from input.input_handler import parse_graph_edge_list


def run_floyd_warshall(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    vertices, edges = parse_graph_edge_list(input_data.get("edges", ""))
    is_directed = input_data.get("directed", True)
    n = len(vertices)
    idx_map = {v: i for i, v in enumerate(vertices)}

    triple_loops = 0
    matrix_updates = 0

    if mode == "silent":
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for e in edges:
            u, v, w = idx_map[e["u"]], idx_map[e["v"]], e["weight"]
            dist[u][v] = min(dist[u][v], w)
            if not is_directed:
                dist[v][u] = min(dist[v][u], w)

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    triple_loops += 1
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        matrix_updates += 1
        return {"output": dist, "solution": dist, "counters": {"triple_loops": triple_loops, "matrix_updates": matrix_updates}}

    def generator():
        nonlocal triple_loops, matrix_updates
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for e in edges:
            u, v, w = idx_map[e["u"]], idx_map[e["v"]], e["weight"]
            dist[u][v] = min(dist[u][v], w)
            if not is_directed:
                dist[v][u] = min(dist[v][u], w)

        nodes_data = [{"id": v, "label": v} for v in vertices]

        def get_formatted_matrix(d_mat):
            return [[(str(val) if val != float('inf') else "∞") for val in row] for row in d_mat]

        yield {
            "type": "init",
            "message": f"Initializing Floyd-Warshall distance matrix of size {n}x{n}.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "distance_matrix": get_formatted_matrix(dist),
                "row_labels": vertices,
                "col_labels": vertices,
                "k_vertex": None
            },
            "counters": {"triple_loops": 0, "matrix_updates": 0}
        }

        for k in range(n):
            k_name = vertices[k]
            yield {
                "type": "pivot_vertex",
                "message": f"Using vertex '{k_name}' (k={k}) as intermediate node.",
                "state": {
                    "nodes": nodes_data,
                    "edges": edges,
                    "distance_matrix": get_formatted_matrix(dist),
                    "row_labels": vertices,
                    "col_labels": vertices,
                    "k_vertex": k_name
                },
                "counters": {}
            }

            for i in range(n):
                for j in range(n):
                    triple_loops += 1
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        matrix_updates += 1
                        u_name, v_name = vertices[i], vertices[j]
                        yield {
                            "type": "matrix_update",
                            "message": f"Updated dist[{u_name}][{v_name}] via '{k_name}' to {dist[i][j]}.",
                            "state": {
                                "nodes": nodes_data,
                                "edges": edges,
                                "distance_matrix": get_formatted_matrix(dist),
                                "row_labels": vertices,
                                "col_labels": vertices,
                                "k_vertex": k_name,
                                "cell": [i, j]
                            },
                            "counters": {"triple_loops": 1, "matrix_updates": 1}
                        }

        yield {
            "type": "done",
            "message": "Floyd-Warshall complete. All-pairs shortest distance matrix computed.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "distance_matrix": get_formatted_matrix(dist),
                "row_labels": vertices,
                "col_labels": vertices,
                "k_vertex": None
            },
            "counters": {}
        }

    return generator(), {}
