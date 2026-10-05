from typing import Any, Dict, List, Tuple
from input.input_handler import parse_graph_edge_list


def run_bellman_ford(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    vertices, edges = parse_graph_edge_list(input_data.get("edges", ""))
    start_node = input_data.get("start", vertices[0])
    is_directed = input_data.get("directed", True)

    n_v = len(vertices)
    iterations = 0
    edge_relaxations = 0

    if mode == "silent":
        dist = {v: float('inf') for v in vertices}
        dist[start_node] = 0
        for i in range(n_v - 1):
            iterations += 1
            updated = False
            for e in edges:
                u, v, w = e["u"], e["v"], e["weight"]
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    edge_relaxations += 1
                    updated = True
                if not is_directed and dist[v] != float('inf') and dist[v] + w < dist[u]:
                    dist[u] = dist[v] + w
                    edge_relaxations += 1
                    updated = True
            if not updated:
                break
        return {"output": dist, "solution": dist, "counters": {"iterations": iterations, "edge_relaxations": edge_relaxations}}

    def generator():
        nonlocal iterations, edge_relaxations
        dist = {v: float('inf') for v in vertices}
        dist[start_node] = 0
        nodes_data = [{"id": v, "label": v} for v in vertices]
        edge_states = {}

        yield {
            "type": "init",
            "message": f"Starting Bellman-Ford Algorithm from source '{start_node}'.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {start_node: "current"},
                "edge_states": edge_states,
                "distance_table": {v: ("0" if v == start_node else "∞") for v in vertices}
            },
            "counters": {"iterations": 0, "edge_relaxations": 0}
        }

        for i in range(n_v - 1):
            iterations += 1
            updated = False

            yield {
                "type": "iteration_start",
                "message": f"Starting relaxation pass {i+1} of {n_v-1}.",
                "state": {
                    "nodes": nodes_data,
                    "edges": edges,
                    "node_states": {},
                    "edge_states": edge_states,
                    "distance_table": {v: (str(dist[v]) if dist[v] != float('inf') else "∞") for v in vertices}
                },
                "counters": {"iterations": 1}
            }

            for e in edges:
                u, v, w = e["u"], e["v"], e["weight"]
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    edge_relaxations += 1
                    updated = True
                    edge_states[(u, v)] = "selected"

                    yield {
                        "type": "relax_edge",
                        "message": f"Relaxed edge ({u} -> {v}): updated dist[{v}] to {dist[v]}.",
                        "state": {
                            "nodes": nodes_data,
                            "edges": edges,
                            "node_states": {u: "current", v: "visited"},
                            "edge_states": dict(edge_states),
                            "distance_table": {node: (str(dist[node]) if dist[node] != float('inf') else "∞") for node in vertices}
                        },
                        "counters": {"edge_relaxations": 1}
                    }

            if not updated:
                yield {
                    "type": "early_stop",
                    "message": f"No distances changed in pass {i+1}. Stopping early.",
                    "state": {
                        "nodes": nodes_data,
                        "edges": edges,
                        "node_states": {},
                        "edge_states": edge_states,
                        "distance_table": {v: (str(dist[v]) if dist[v] != float('inf') else "∞") for v in vertices}
                    },
                    "counters": {}
                }
                break

        yield {
            "type": "done",
            "message": f"Bellman-Ford complete. Final Shortest Distances: {dist}.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {v: "visited" for v in vertices},
                "edge_states": edge_states,
                "distance_table": {v: (str(dist[v]) if dist[v] != float('inf') else "∞") for v in vertices}
            },
            "counters": {}
        }

    return generator(), {}
