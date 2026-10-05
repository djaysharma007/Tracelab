from typing import Any, Dict, List, Tuple
from input.input_handler import parse_graph_edge_list


def run_dfs(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    vertices, edges = parse_graph_edge_list(input_data.get("edges", ""))
    start_node = input_data.get("start", vertices[0])
    is_directed = input_data.get("directed", False)

    adj = {v: [] for v in vertices}
    for e in edges:
        adj[e["u"]].append(e["v"])
        if not is_directed:
            adj[e["v"]].append(e["u"])

    node_visits = 0
    edge_traversals = 0

    if mode == "silent":
        visited = set()
        stack = [start_node]
        order = []
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                order.append(curr)
                node_visits += 1
                for neighbor in reversed(adj[curr]):
                    edge_traversals += 1
                    if neighbor not in visited:
                        stack.append(neighbor)
        return {"output": order, "solution": order, "counters": {"node_visits": node_visits, "edge_traversals": edge_traversals}}

    def generator():
        nonlocal node_visits, edge_traversals
        visited = set()
        stack = [start_node]
        order = []
        edge_states = {}
        nodes_data = [{"id": v, "label": v} for v in vertices]

        yield {
            "type": "init",
            "message": f"Starting DFS traversal from source node '{start_node}'.",
            "state": {
                "nodes": nodes_data,
                "edges": edges,
                "node_states": {start_node: "current"},
                "edge_states": edge_states,
                "queue_or_stack": list(stack),
                "visited": []
            },
            "counters": {"node_visits": 0, "edge_traversals": 0}
        }

        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                order.append(curr)
                node_visits += 1

                yield {
                    "type": "visit_node",
                    "message": f"Popped and visiting node '{curr}'. Order: {order}.",
                    "state": {
                        "nodes": nodes_data,
                        "edges": edges,
                        "node_states": {v: "visited" if v in visited else ("current" if v == curr else "default") for v in vertices},
                        "edge_states": edge_states,
                        "queue_or_stack": list(stack),
                        "visited": list(order)
                    },
                    "counters": {"node_visits": 1}
                }

                for neighbor in reversed(adj[curr]):
                    edge_traversals += 1
                    if neighbor not in visited:
                        stack.append(neighbor)
                        yield {
                            "type": "push_stack",
                            "message": f"Pushing unvisited neighbor '{neighbor}' onto DFS stack.",
                            "state": {
                                "nodes": nodes_data,
                                "edges": edges,
                                "node_states": {v: "visited" if v in visited else "default" for v in vertices},
                                "edge_states": edge_states,
                                "queue_or_stack": list(stack),
                                "visited": list(order)
                            },
                            "counters": {"edge_traversals": 1}
                        }

        yield {
            "type": "done",
            "message": f"DFS Traversal complete. Traversal Order: {order}.",
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
