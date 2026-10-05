from typing import Any, Dict, List, Tuple
from input.input_handler import parse_graph_edge_list


class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        if self.parent[item] == item:
            return item
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True
        return False


def run_kruskal(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    vertices, edges = parse_graph_edge_list(input_data.get("edges", ""))
    sorted_edges = sorted(edges, key=lambda e: e["weight"])

    edge_evaluations = 0
    union_find_ops = 0

    if mode == "silent":
        dsu = DisjointSet(vertices)
        mst_cost = 0
        count = 0
        for e in sorted_edges:
            edge_evaluations += 1
            union_find_ops += 1
            if dsu.union(e["u"], e["v"]):
                mst_cost += e["weight"]
                count += 1
                if count == len(vertices) - 1:
                    break
        return {"output": mst_cost, "solution": mst_cost, "counters": {"edge_evaluations": edge_evaluations, "union_find_ops": union_find_ops}}

    def generator():
        nonlocal edge_evaluations, union_find_ops
        dsu = DisjointSet(vertices)
        mst_cost = 0
        mst_edges = []
        edge_states = {}
        nodes_data = [{"id": v, "label": v} for v in vertices]

        yield {
            "type": "init",
            "message": f"Starting Kruskal's MST Algorithm. Sorted {len(sorted_edges)} edges by weight.",
            "state": {
                "nodes": nodes_data,
                "edges": sorted_edges,
                "node_states": {},
                "edge_states": edge_states,
                "mst_edges": [],
                "mst_cost": 0
            },
            "counters": {"edge_evaluations": 0, "union_find_ops": 0}
        }

        for e in sorted_edges:
            u, v, w = e["u"], e["v"], e["weight"]
            edge_evaluations += 1
            union_find_ops += 1

            if dsu.union(u, v):
                mst_cost += w
                mst_edges.append(e)
                edge_states[(u, v)] = "selected"
                edge_states[(v, u)] = "selected"

                yield {
                    "type": "add_mst_edge",
                    "message": f"Accepted edge ({u} - {v}: {w}) - doesn't form a cycle. MST Cost = {mst_cost}.",
                    "state": {
                        "nodes": nodes_data,
                        "edges": sorted_edges,
                        "node_states": {u: "visited", v: "visited"},
                        "edge_states": dict(edge_states),
                        "mst_edges": list(mst_edges),
                        "mst_cost": mst_cost
                    },
                    "counters": {"edge_evaluations": 1, "union_find_ops": 1}
                }

                if len(mst_edges) == len(vertices) - 1:
                    break
            else:
                edge_states[(u, v)] = "rejected"
                edge_states[(v, u)] = "rejected"
                yield {
                    "type": "reject_edge",
                    "message": f"Rejected edge ({u} - {v}: {w}) - forms a cycle in DSU.",
                    "state": {
                        "nodes": nodes_data,
                        "edges": sorted_edges,
                        "node_states": {},
                        "edge_states": dict(edge_states),
                        "mst_edges": list(mst_edges),
                        "mst_cost": mst_cost
                    },
                    "counters": {"edge_evaluations": 1, "union_find_ops": 1}
                }

        yield {
            "type": "done",
            "message": f"Kruskal's Algorithm complete. Minimum Spanning Tree Cost = {mst_cost}.",
            "state": {
                "nodes": nodes_data,
                "edges": sorted_edges,
                "node_states": {v: "visited" for v in vertices},
                "edge_states": edge_states,
                "mst_edges": mst_edges,
                "mst_cost": mst_cost
            },
            "counters": {}
        }

    return generator(), 0
