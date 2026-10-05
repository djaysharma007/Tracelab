import heapq
from collections import Counter
from typing import Any, Dict, List, Tuple


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def run_huffman_coding(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    text = str(input_data["text"])
    freq_map = dict(Counter(text))

    tree_merges = 0
    priority_queue_ops = 0

    if mode == "silent":
        pq = [HuffmanNode(c, f) for c, f in freq_map.items()]
        heapq.heapify(pq)
        priority_queue_ops += len(pq)

        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(pq, merged)
            tree_merges += 1
            priority_queue_ops += 3

        codes = {}
        root = pq[0] if pq else None

        def build_codes(node, curr_code):
            if not node:
                return
            if node.char is not None:
                codes[node.char] = curr_code or "0"
                return
            build_codes(node.left, curr_code + "0")
            build_codes(node.right, curr_code + "1")

        build_codes(root, "")
        return {"output": codes, "solution": codes, "counters": {"tree_merges": tree_merges, "priority_queue_ops": priority_queue_ops}}

    def generator():
        nonlocal tree_merges, priority_queue_ops
        pq = [HuffmanNode(c, f) for c, f in freq_map.items()]
        heapq.heapify(pq)
        priority_queue_ops += len(pq)

        def node_to_dict(node):
            if not node:
                return None
            return {
                "char": node.char,
                "freq": node.freq,
                "left": node_to_dict(node.left),
                "right": node_to_dict(node.right)
            }

        yield {
            "type": "init",
            "message": f"Calculated char frequencies for '{text}': {freq_map}.",
            "state": {
                "frequencies": freq_map,
                "queue": [f"'{n.char}':{n.freq}" for n in sorted(pq)],
                "tree": None,
                "codes": {}
            },
            "counters": {"tree_merges": 0, "priority_queue_ops": priority_queue_ops}
        }

        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            l_label = f"'{left.char}'" if left.char else f"Subtree({left.freq})"
            r_label = f"'{right.char}'" if right.char else f"Subtree({right.freq})"

            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(pq, merged)
            tree_merges += 1
            priority_queue_ops += 3

            yield {
                "type": "merge_nodes",
                "message": f"Merged two lowest frequency nodes: {l_label} ({left.freq}) + {r_label} ({right.freq}) -> {merged.freq}.",
                "state": {
                    "frequencies": freq_map,
                    "queue": [f"'{n.char or 'Internal'}':{n.freq}" for n in sorted(pq)],
                    "tree": node_to_dict(merged),
                    "codes": {}
                },
                "counters": {"tree_merges": 1, "priority_queue_ops": 3}
            }

        root = pq[0] if pq else None
        codes = {}

        def build_codes(node, curr_code):
            if not node:
                return
            if node.char is not None:
                codes[node.char] = curr_code or "0"
                return
            build_codes(node.left, curr_code + "0")
            build_codes(node.right, curr_code + "1")

        build_codes(root, "")

        yield {
            "type": "done",
            "message": f"Huffman Coding tree construction complete. Generated Codes: {codes}.",
            "state": {
                "frequencies": freq_map,
                "queue": [],
                "tree": node_to_dict(root),
                "codes": codes
            },
            "counters": {}
        }

    return generator(), {}
