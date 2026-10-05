from collections import deque
from typing import Any, Dict, List, Tuple
from input.input_handler import parse_graph_edge_list


def run_bfs(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    vertices, edges = parse_graph_edge_list(input_data.get("edges", ""))
    start_node = input_data.get("start", vertices[0])
    is_directed = input_data.get("directed", False)

    # Build adjacency list
    adj = {v: [] for v in vertices}
    for e in edges:
        adj[e["u"]].append(e["v"])
        if not is_directed:
            adj[e["v"]].append(e["u"])

    node_visits = 0
    edge_traversals = 0

    if mode == "silent":
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        order = []
        while queue:
            curr = queue.popleft()
            order.append(curr)
            node_visits += 1
            for neighbor in adj[curr]:
                edge_traversals += 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return {"output": order, "solution": order, "counters": {"node_visits": node_visits, "edge_traversals": edge_traversals}}

    def generator():
        nonlocal node_visits, edge_traversals
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        order = []
        edge_states = {(e["u"], e["v"]): "default" for e in edges}

        nodes_data = [{"id": v, "label": v} for v in vertices]

        yield {
            "type": "init",
            "message": f"Starting BFS traversal from source node '{start_node}'.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {start_node: "current"},
                "edge_states": edge_states,
                "queue_or_stack": list(queue),
                "visited": sorted(list(visited))
            },
            "counters": {"node_visits": 0, "edge_traversals": 0}
        }

        while queue:
            curr = queue.popleft()
            order.append(curr)
            node_visits += 1

            yield {
                "type": "visit_node",
                "message": f"Dequeued and visiting node '{curr}'. Order: {order}.",
                "state": {
                    "nodes": nodes_data,
                    "edges": edges,
                    "node_states": {v: "visited" if v in visited else ("current" if v == curr else "default") for v in vertices},
                    "edge_states": edge_states,
                    "queue_or_stack": list(queue),
                    "visited": sorted(list(visited))
                },
                "counters": {"node_visits": 1}
            }

            for neighbor in adj[curr]:
                edge_traversals += 1
                is_new = (neighbor not in visited)
                edge_states[(curr, neighbor)] = "selected" if is_new else "considering"
                if not is_directed:
                    edge_states[(neighbor, curr)] = "selected" if is_new else "considering"

                if is_new:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    yield {
                        "type": "enqueue",
                        "message": f"Discovered unvisited neighbor '{neighbor}' from '{curr}'. Enqueuing '{neighbor}'.",
                        "state": {
                            "nodes": nodes_data,
                            "edges": edges,
                            "node_states": {v: ("visited" if v in visited else "default") for v in vertices},
                            "edge_states": dict(edge_states),
                            "queue_or_stack": list(queue),
                            "visited": sorted(list(visited))
                        },
                        "counters": {"edge_traversals": 1}
                    }

        yield {
            "type": "done",
            "message": f"BFS Traversal complete. Traversal Order: {order}.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {v: "visited" for v in order},
                "edge_states": edge_states,
                "queue_or_stack": [],
                "visited": order
            },
            "counters": {}
        }

    return generator(), []
