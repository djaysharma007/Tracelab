import random
from typing import Any, Dict, List, Optional


def generate_input_for_algorithm(
    kind: str,
    size: int,
    rand_inst: Optional[random.Random] = None,
    input_type: str = "random"  # "random", "sorted", "reverse", "duplicates", "nearly_sorted", "not_found", "worst_case", "no_match", "dense", "sparse"
) -> Dict[str, Any]:
    r = rand_inst or random.Random()

    if kind in ["array", "sorting"]:
        if input_type in ["sorted", "best_case"]:
            arr = list(range(1, size + 1))
        elif input_type in ["reverse", "worst_case"]:
            arr = list(range(size, 0, -1))
        elif input_type == "duplicates":
            num_unique = max(2, size // 4)
            arr = [r.randint(1, num_unique) * 10 for _ in range(size)]
        elif input_type == "nearly_sorted":
            arr = list(range(1, size + 1))
            num_swaps = max(1, size // 10)
            for _ in range(num_swaps):
                i, j = r.randint(0, size - 1), r.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]
        else:
            arr = [r.randint(1, size * 5) for _ in range(size)]
        return {"array": arr}

    elif kind == "searching":
        if input_type == "reverse":
            arr = list(range(size * 2, 0, -2))
        elif input_type == "duplicates":
            num_unique = max(2, size // 3)
            arr = sorted([r.randint(1, num_unique) * 5 for _ in range(size)])
        else:
            arr = sorted([r.randint(1, size * 5) for _ in range(size)])

        if input_type == "not_found":
            target = size * 5 + 99
        else:
            target = arr[r.randint(0, size - 1)] if arr else 10
        return {"array": arr, "target": target}

    elif kind == "string":
        if input_type in ["worst_case", "duplicates"]:
            # e.g., AAAAAAAAAB vs AAAB
            text = "A" * (max(10, size) - 1) + "B"
            pattern = "A" * max(2, min(size // 3, 5)) + "B"
        elif input_type == "no_match":
            text = "A" * max(10, size)
            pattern = "A" * (max(2, min(size // 3, 5)) - 1) + "B"
        elif input_type in ["multiple", "sorted"]:
            pat = "AABA"
            text = (pat * (size // len(pat) + 1))[:size]
            pattern = pat
        else:
            chars = ["A", "B", "C", "D"]
            text_len = max(size, 10)
            pattern_len = max(2, min(size // 3, 6))
            text = "".join(r.choice(chars) for _ in range(text_len))
            if r.random() > 0.3 and text_len >= pattern_len:
                start_pos = r.randint(0, text_len - pattern_len)
                pattern = text[start_pos: start_pos + pattern_len]
            else:
                pattern = "".join(r.choice(chars) for _ in range(pattern_len))
        return {"text": text, "pattern": pattern}

    elif kind == "dp_knapsack":
        n = max(3, min(size, 15))
        if input_type == "duplicates":
            weights = [3] * n
            values = [10] * n
        else:
            weights = [r.randint(1, 10) for _ in range(n)]
            values = [r.randint(10, 100) for _ in range(n)]
        capacity = sum(weights) // 2
        return {"weights": weights, "values": values, "capacity": capacity}

    elif kind in ["dp_lcs", "dp_edit_distance"]:
        chars = ["A", "B", "C", "D", "E"]
        len1 = max(3, min(size, 12))
        len2 = max(3, min(size, 12))
        if input_type == "sorted":
            str1 = "ABCDE" * (len1 // 5 + 1)
            str2 = "ABCDE" * (len2 // 5 + 1)
            str1, str2 = str1[:len1], str2[:len2]
        else:
            str1 = "".join(r.choice(chars) for _ in range(len1))
            str2 = "".join(r.choice(chars) for _ in range(len2))
        return {"str1": str1, "str2": str2}

    elif kind == "dp_lis":
        n = max(5, min(size, 20))
        if input_type == "sorted":
            arr = list(range(1, n + 1))
        elif input_type == "reverse":
            arr = list(range(n, 0, -1))
        else:
            arr = [r.randint(1, 50) for _ in range(n)]
        return {"array": arr}

    elif kind == "dp_mcm":
        n = max(3, min(size, 8))
        dims = [r.randint(5, 30) for _ in range(n + 1)]
        return {"dimensions": dims}

    elif kind == "graph":
        num_vertices = max(4, min(size, 12))
        vertices = [chr(65 + i) for i in range(num_vertices)]
        edges_list = []

        if input_type == "sparse":
            # Path graph
            for i in range(num_vertices - 1):
                w = r.randint(1, 10)
                edges_list.append(f"{vertices[i]} {vertices[i+1]} {w}")
        elif input_type == "dense":
            # Complete graph
            for i in range(num_vertices):
                for j in range(i + 1, num_vertices):
                    w = r.randint(1, 10)
                    edges_list.append(f"{vertices[i]} {vertices[j]} {w}")
        else:
            # Random connected graph
            for i in range(num_vertices - 1):
                w = r.randint(1, 10)
                edges_list.append(f"{vertices[i]} {vertices[i+1]} {w}")
            for _ in range(num_vertices):
                u, v = r.sample(vertices, 2)
                w = r.randint(1, 10)
                edges_list.append(f"{u} {v} {w}")

        return {"edges": "\n".join(edges_list), "start": vertices[0], "directed": False}

    elif kind == "greedy_activity":
        n = max(4, min(size, 15))
        activities = []
        for i in range(n):
            s = r.randint(0, 15)
            f = s + r.randint(1, 6)
            activities.append({"name": f"a{i+1}", "start": s, "finish": f})
        return {"activities": activities}

    elif kind == "greedy_knapsack":
        n = max(3, min(size, 12))
        items = []
        for i in range(n):
            w = r.randint(5, 25)
            v = r.randint(20, 100)
            items.append({"name": f"Item {i+1}", "weight": w, "value": v})
        capacity = 50
        return {"items": items, "capacity": capacity}

    elif kind == "greedy_huffman":
        words = ["abracadabra", "hello world", "trace lab python react", "algorithm analysis"]
        return {"text": r.choice(words)}

    elif kind == "greedy_jobs":
        n = max(4, min(size, 10))
        jobs = []
        for i in range(n):
            d = r.randint(1, min(n, 5))
            p = r.randint(10, 100)
            jobs.append({"id": f"j{i+1}", "deadline": d, "profit": p})
        return {"jobs": jobs}

    # Default fallback
    return {"array": [r.randint(1, 100) for _ in range(max(5, size))]}
