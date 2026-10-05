import heapq
from typing import Any, Dict, List, Tuple
from input.input_handler import parse_graph_edge_list


def run_dijkstra(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    vertices, edges = parse_graph_edge_list(input_data.get("edges", ""))
    start_node = input_data.get("start", vertices[0])
    is_directed = input_data.get("directed", False)

    adj = {v: [] for v in vertices}
    for e in edges:
        adj[e["u"]].append((e["v"], e["weight"]))
        if not is_directed:
            adj[e["v"]].append((e["u"], e["weight"]))

    node_visits = 0
    edge_relaxations = 0

    if mode == "silent":
        dist = {v: float('inf') for v in vertices}
        dist[start_node] = 0
        pq = [(0, start_node)]
        visited = set()

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            node_visits += 1

            for v, weight in adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    edge_relaxations += 1
                    heapq.heappush(pq, (dist[v], v))
        return {"output": dist, "solution": dist, "counters": {"node_visits": node_visits, "edge_relaxations": edge_relaxations}}

    def generator():
        nonlocal node_visits, edge_relaxations
        dist = {v: float('inf') for v in vertices}
        parent = {v: None for v in vertices}
        dist[start_node] = 0
        pq = [(0, start_node)]
        visited = set()
        edge_states = {}
        nodes_data = [{"id": v, "label": v} for v in vertices]

        yield {
            "type": "init",
            "message": f"Starting Dijkstra's Algorithm from source node '{start_node}'.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {start_node: "current"},
                "edge_states": edge_states,
                "queue_or_stack": [f"{v}: {d}" for d, v in pq],
                "distance_table": {v: ("0" if v == start_node else "∞") for v in vertices}
            },
            "counters": {"node_visits": 0, "edge_relaxations": 0}
        }

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            node_visits += 1

            yield {
                "type": "visit_node",
                "message": f"Popped node '{u}' with min distance {d}.",
                "state": {
                    "nodes": nodes_data,
                    "edges": edges,
                    "node_states": {v: ("visited" if v in visited else ("current" if v == u else "default")) for v in vertices},
                    "edge_states": edge_states,
                    "queue_or_stack": [f"{v}: {dist[v]}" for dist_val, v in pq if v not in visited],
                    "distance_table": {v: (str(dist[v]) if dist[v] != float('inf') else "∞") for v in vertices}
                },
                "counters": {"node_visits": 1}
            }

            for v, weight in adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    edge_relaxations += 1
                    heapq.heappush(pq, (dist[v], v))
                    edge_states[(u, v)] = "selected"

                    yield {
                        "type": "relax_edge",
                        "message": f"Relaxed edge ({u} -> {v}): updated dist[{v}] to {dist[v]}.",
                        "state": {
                            "nodes": nodes_data,
                            "edges": edges,
                            "node_states": {node: ("visited" if node in visited else "default") for node in vertices},
                            "edge_states": dict(edge_states),
                            "queue_or_stack": [f"{node}: {dist[node]}" for dist_val, node in pq if node not in visited],
                            "distance_table": {node: (str(dist[node]) if dist[node] != float('inf') else "∞") for node in vertices}
                        },
                        "counters": {"edge_relaxations": 1}
                    }

        yield {
            "type": "done",
            "message": f"Dijkstra complete. Shortest Distances: {dist}.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {v: "visited" for v in vertices},
                "edge_states": edge_states,
                "queue_or_stack": [],
                "distance_table": {v: (str(dist[v]) if dist[v] != float('inf') else "∞") for v in vertices}
            },
            "counters": {}
        }

    return generator(), {}
