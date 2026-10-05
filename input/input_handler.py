from typing import Any, Dict, List, Tuple


def parse_graph_edge_list(edges_str: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Parses edge list text like:
    A B 4
    B C 2
    or
    A B
    Returns sorted unique vertices list and parsed edge objects list.
    """
    if not edges_str or not edges_str.strip():
        raise ValueError("Edge list cannot be empty.")

    lines = [line.strip() for line in edges_str.strip().split("\n") if line.strip()]
    if not lines:
        raise ValueError("No valid edges found in input.")

    vertices = set()
    edges = []

    for idx, line in enumerate(lines, 1):
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"Line {idx} '{line}' must contain at least source and target vertices.")
        u, v = parts[0], parts[1]
        weight = 1.0
        if len(parts) >= 3:
            try:
                weight = float(parts[2])
            except ValueError:
                raise ValueError(f"Line {idx} weight '{parts[2]}' must be a valid number.")

        vertices.add(u)
        vertices.add(v)
        edges.append({"u": u, "v": v, "weight": weight})

    sorted_vertices = sorted(list(vertices))
    return sorted_vertices, edges


def validate_algorithm_input(alg_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates input structure and values for the specified algorithm.
    Raises ValueError with specific plain English explanation if invalid.
    """
    if alg_id in ["bubble_sort", "selection_sort", "insertion_sort", "merge_sort", "quick_sort", "heap_sort", "dp_lis"]:
        if "array" not in input_data or not isinstance(input_data["array"], list):
            raise ValueError("Input must contain an 'array' field with a list of numbers.")
        if len(input_data["array"]) == 0:
            raise ValueError("Array cannot be empty.")

    elif alg_id in ["linear_search", "binary_search"]:
        if "array" not in input_data or not isinstance(input_data["array"], list):
            raise ValueError("Input must contain an 'array' list.")
        if "target" not in input_data:
            raise ValueError("Input must specify a 'target' value to search for.")
        if len(input_data["array"]) == 0:
            raise ValueError("Array cannot be empty.")
        if alg_id == "binary_search":
            # Check if sorted
            arr = input_data["array"]
            is_sorted = all(arr[i] <= arr[i+1] for i in range(len(arr)-1))
            if not is_sorted:
                raise ValueError("Binary Search requires a sorted array. Please sort your array or choose Linear Search.")

    elif alg_id in ["naive_search", "rabin_karp", "kmp_search", "z_search"]:
        if "text" not in input_data or not isinstance(input_data["text"], str):
            raise ValueError("Input must contain a 'text' string.")
        if "pattern" not in input_data or not isinstance(input_data["pattern"], str):
            raise ValueError("Input must contain a 'pattern' string.")
        if len(input_data["text"]) == 0:
            raise ValueError("Text string cannot be empty.")
        if len(input_data["pattern"]) == 0:
            raise ValueError("Pattern string cannot be empty.")
        if len(input_data["pattern"]) > len(input_data["text"]):
            raise ValueError("Pattern length cannot be greater than text length.")

    elif alg_id == "knapsack_01":
        weights = input_data.get("weights")
        values = input_data.get("values")
        capacity = input_data.get("capacity")
        if not weights or not values or capacity is None:
            raise ValueError("Knapsack input requires 'weights', 'values', and 'capacity'.")
        if len(weights) != len(values):
            raise ValueError("Weights list and Values list must be of the same length.")

    elif alg_id in ["lcs", "edit_distance"]:
        str1 = input_data.get("str1")
        str2 = input_data.get("str2")
        if str1 is None or str2 is None:
            raise ValueError("Input requires 'str1' and 'str2' strings.")

    elif alg_id == "mcm":
        dims = input_data.get("dimensions")
        if not dims or len(dims) < 2:
            raise ValueError("Matrix Chain Multiplication requires at least 2 matrix dimensions (e.g., [10, 30, 5]).")

    elif alg_id in ["bfs", "dfs", "dijkstra", "bellman_ford", "floyd_warshall", "prim", "kruskal"]:
        edges_str = input_data.get("edges", "")
        vertices, edges = parse_graph_edge_list(edges_str)
        if alg_id in ["bfs", "dfs", "dijkstra", "bellman_ford", "prim"]:
            start = input_data.get("start")
            if not start:
                input_data["start"] = vertices[0]
            elif input_data["start"] not in vertices:
                raise ValueError(f"Start vertex '{input_data['start']}' is not present in the graph vertices {vertices}.")

    elif alg_id == "activity_selection":
        activities = input_data.get("activities")
        if not activities or not isinstance(activities, list):
            raise ValueError("Input must contain an 'activities' list.")

    elif alg_id == "fractional_knapsack":
        items = input_data.get("items")
        capacity = input_data.get("capacity")
        if not items or capacity is None:
            raise ValueError("Fractional Knapsack requires 'items' list and 'capacity'.")

    elif alg_id == "huffman_coding":
        text = input_data.get("text")
        if not text or not isinstance(text, str):
            raise ValueError("Huffman Coding requires a non-empty 'text' string.")

    elif alg_id == "job_sequencing":
        jobs = input_data.get("jobs")
        if not jobs or not isinstance(jobs, list):
            raise ValueError("Job Sequencing requires a list of 'jobs'.")

    return input_data
