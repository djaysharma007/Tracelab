import heapq
from typing import Any, Dict, List, Tuple
from input.input_handler import parse_graph_edge_list


def run_prim(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    vertices, edges = parse_graph_edge_list(input_data.get("edges", ""))
    start_node = input_data.get("start", vertices[0])

    adj = {v: [] for v in vertices}
    for e in edges:
        adj[e["u"]].append((e["v"], e["weight"]))
        adj[e["v"]].append((e["u"], e["weight"]))

    node_visits = 0
    edge_evaluations = 0

    if mode == "silent":
        mst_cost = 0
        visited = set([start_node])
        pq = [(weight, start_node, neighbor) for neighbor, weight in adj[start_node]]
        heapq.heapify(pq)

        while pq and len(visited) < len(vertices):
            weight, u, v = heapq.heappop(pq)
            edge_evaluations += 1
            if v not in visited:
                visited.add(v)
                mst_cost += weight
                node_visits += 1
                for next_v, next_w in adj[v]:
                    if next_v not in visited:
                        heapq.heappush(pq, (next_w, v, next_v))
        return {"output": mst_cost, "solution": mst_cost, "counters": {"node_visits": node_visits, "edge_evaluations": edge_evaluations}}

    def generator():
        nonlocal node_visits, edge_evaluations
        mst_cost = 0
        visited = set([start_node])
        pq = [(weight, start_node, neighbor) for neighbor, weight in adj[start_node]]
        heapq.heapify(pq)

        mst_edges = []
        edge_states = {}
        nodes_data = [{"id": v, "label": v} for v in vertices]

        yield {
            "type": "init",
            "message": f"Starting Prim's MST Algorithm from vertex '{start_node}'.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {start_node: "visited"},
                "edge_states": edge_states,
                "mst_edges": [],
                "queue_or_stack": [f"({u}-{v}: {w})" for w, u, v in pq],
                "mst_cost": 0
            },
            "counters": {"node_visits": 1, "edge_evaluations": 0}
        }

        while pq and len(visited) < len(vertices):
            weight, u, v = heapq.heappop(pq)
            edge_evaluations += 1

            if v not in visited:
                visited.add(v)
                mst_cost += weight
                node_visits += 1
                mst_edges.append({"u": u, "v": v, "weight": weight})
                edge_states[(u, v)] = "selected"
                edge_states[(v, u)] = "selected"

                for next_v, next_w in adj[v]:
                    if next_v not in visited:
                        heapq.heappush(pq, (next_w, v, next_v))

                yield {
                    "type": "add_mst_edge",
                    "message": f"Added minimum weight edge ({u} - {v}: {weight}) to MST. Current Total Cost = {mst_cost}.",
                    "state": {
                        "nodes": nodes_data,
                        "edges": edges,
                        "node_states": {node: ("visited" if node in visited else "default") for node in vertices},
                        "edge_states": dict(edge_states),
                        "mst_edges": list(mst_edges),
                        "queue_or_stack": [f"({n1}-{n2}: {w})" for w, n1, n2 in pq if n2 not in visited],
                        "mst_cost": mst_cost
                    },
                    "counters": {"node_visits": 1, "edge_evaluations": 1}
                }
            else:
                edge_states[(u, v)] = "rejected"
                edge_states[(v, u)] = "rejected"
                yield {
                    "type": "reject_edge",
                    "message": f"Rejected edge ({u} - {v}: {weight}) because vertex '{v}' is already in MST.",
                    "state": {
                        "nodes": nodes_data,
                        "edges": edges,
                        "node_states": {node: ("visited" if node in visited else "default") for node in vertices},
                        "edge_states": dict(edge_states),
                        "mst_edges": list(mst_edges),
                        "queue_or_stack": [f"({n1}-{n2}: {w})" for w, n1, n2 in pq if n2 not in visited],
                        "mst_cost": mst_cost
                    },
                    "counters": {"edge_evaluations": 1}
                }

        yield {
            "type": "done",
            "message": f"Prim's Algorithm complete. Minimum Spanning Tree Cost = {mst_cost}.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {v: "visited" for v in vertices},
                "edge_states": edge_states,
                "mst_edges": mst_edges,
                "queue_or_stack": [],
                "mst_cost": mst_cost
            },
            "counters": {}
        }

    return generator(), 0
