from typing import Dict, List, Optional
from core.models import AlgorithmMetadata, InputSchemaDef, PresetDef


ALGORITHM_REGISTRY: Dict[str, AlgorithmMetadata] = {
    # --- SORTING ---
    "bubble_sort": AlgorithmMetadata(
        id="bubble_sort",
        name="Bubble Sort",
        category="Sorting",
        compare_group="Sorting",
        stage="array",
        description="Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
        complexity={
            "best": "O(n)",
            "average": "O(n²)",
            "worst": "O(n²)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="array",
            description="Array of integers or floating point numbers.",
            fields={"array": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Unsorted Array", input={"array": [45, 12, 89, 34, 67, 23, 90, 11]}),
            PresetDef(name="sorted", label="Already Sorted", input={"array": [10, 20, 30, 40, 50, 60, 70, 80]}),
            PresetDef(name="reverse", label="Reverse Sorted", input={"array": [80, 70, 60, 50, 40, 30, 20, 10]}),
            PresetDef(name="duplicates", label="Many Duplicates", input={"array": [30, 10, 30, 20, 10, 30, 20, 10]})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "swaps", "iterations"]
    ),
    "selection_sort": AlgorithmMetadata(
        id="selection_sort",
        name="Selection Sort",
        category="Sorting",
        compare_group="Sorting",
        stage="array",
        description="Divides the input list into two parts: a sorted sublist and an unsorted sublist, repeatedly selecting the smallest element from the unsorted sublist.",
        complexity={
            "best": "O(n²)",
            "average": "O(n²)",
            "worst": "O(n²)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="array",
            description="Array of numbers.",
            fields={"array": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Unsorted Array", input={"array": [64, 25, 12, 22, 11, 90, 45]}),
            PresetDef(name="sorted", label="Already Sorted", input={"array": [11, 12, 22, 25, 45, 64, 90]}),
            PresetDef(name="reverse", label="Reverse Sorted", input={"array": [90, 64, 45, 25, 22, 12, 11]})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "swaps", "iterations"]
    ),
    "insertion_sort": AlgorithmMetadata(
        id="insertion_sort",
        name="Insertion Sort",
        category="Sorting",
        compare_group="Sorting",
        stage="array",
        description="Builds the final sorted array one item at a time by inserting each element into its proper position within the sorted portion.",
        complexity={
            "best": "O(n)",
            "average": "O(n²)",
            "worst": "O(n²)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="array",
            description="Array of numbers.",
            fields={"array": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Unsorted Array", input={"array": [12, 11, 13, 5, 6, 7]}),
            PresetDef(name="sorted", label="Already Sorted", input={"array": [5, 6, 7, 11, 12, 13]}),
            PresetDef(name="reverse", label="Reverse Sorted", input={"array": [13, 12, 11, 7, 6, 5]})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "shifts", "iterations"]
    ),
    "merge_sort": AlgorithmMetadata(
        id="merge_sort",
        name="Merge Sort",
        category="Sorting",
        compare_group="Sorting",
        stage="array",
        description="Divide-and-conquer algorithm that divides the array into two halves, recursively sorts them, and merges the sorted halves.",
        complexity={
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(n)"
        },
        input_schema=InputSchemaDef(
            kind="array",
            description="Array of numbers.",
            fields={"array": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Unsorted Array", input={"array": [38, 27, 43, 3, 9, 82, 10]}),
            PresetDef(name="reverse", label="Reverse Sorted", input={"array": [82, 43, 38, 27, 10, 9, 3]})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "merges", "recursive_calls"]
    ),
    "quick_sort": AlgorithmMetadata(
        id="quick_sort",
        name="Quick Sort",
        category="Sorting",
        compare_group="Sorting",
        stage="array",
        description="Picks an element as a pivot and partitions the array around the pivot so that smaller elements come before it and larger ones after.",
        complexity={
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n²)",
            "space": "O(log n)"
        },
        input_schema=InputSchemaDef(
            kind="array",
            description="Array of numbers.",
            fields={"array": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Unsorted Array", input={"array": [10, 80, 30, 90, 40, 50, 70]}),
            PresetDef(name="sorted", label="Already Sorted", input={"array": [10, 30, 40, 50, 70, 80, 90]})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "swaps", "recursive_calls"]
    ),
    "heap_sort": AlgorithmMetadata(
        id="heap_sort",
        name="Heap Sort",
        category="Sorting",
        compare_group="Sorting",
        stage="array",
        description="Converts the array into a Max-Heap structure and repeatedly extracts the maximum element, restoring the heap property.",
        complexity={
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="array",
            description="Array of numbers.",
            fields={"array": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Unsorted Array", input={"array": [4, 10, 3, 5, 1]}),
            PresetDef(name="reverse", label="Reverse Sorted", input={"array": [10, 5, 4, 3, 1]})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "swaps", "heapify_calls"]
    ),

    # --- SEARCHING ---
    "linear_search": AlgorithmMetadata(
        id="linear_search",
        name="Linear Search",
        category="Searching",
        compare_group="Searching",
        stage="array",
        description="Sequentially checks each element of the list until a match is found or the whole list has been searched.",
        complexity={
            "best": "O(1)",
            "average": "O(n)",
            "worst": "O(n)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="searching",
            description="Array and target value.",
            fields={"array": "List[int]", "target": "int"}
        ),
        presets=[
            PresetDef(name="found", label="Element Present", input={"array": [10, 50, 30, 70, 80, 20], "target": 70}),
            PresetDef(name="not_found", label="Element Absent", input={"array": [10, 50, 30, 70, 80, 20], "target": 99})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "iterations"]
    ),
    "binary_search": AlgorithmMetadata(
        id="binary_search",
        name="Binary Search",
        category="Searching",
        compare_group="Searching",
        stage="array",
        description="Search algorithm that finds the position of a target value within a sorted array by repeatedly halving the search interval.",
        complexity={
            "best": "O(1)",
            "average": "O(log n)",
            "worst": "O(log n)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="searching",
            description="Sorted array and target value.",
            fields={"array": "List[int]", "target": "int"}
        ),
        presets=[
            PresetDef(name="found", label="Element Present", input={"array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], "target": 23}),
            PresetDef(name="not_found", label="Element Absent", input={"array": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], "target": 40})
        ],
        max_visual_size=100,
        max_benchmark_size=10000,
        counters=["comparisons", "iterations"]
    ),

    # --- STRING MATCHING ---
    "naive_search": AlgorithmMetadata(
        id="naive_search",
        name="Naive String Matching",
        category="String matching",
        compare_group="String matching",
        stage="string",
        description="Checks all candidate positions for pattern alignment in text character by character.",
        complexity={
            "best": "O(n)",
            "average": "O(m * (n - m + 1))",
            "worst": "O(m * (n - m + 1))",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="string",
            description="Text string and Pattern string.",
            fields={"text": "str", "pattern": "str"}
        ),
        presets=[
            PresetDef(name="match", label="Single Match", input={"text": "ABABDABACDABABCABAB", "pattern": "ABABCABAB"}),
            PresetDef(name="multiple", label="Multiple Matches", input={"text": "AABAACAADAABAABA", "pattern": "AABA"}),
            PresetDef(name="no_match", label="No Match", input={"text": "AAAAAAAAAAAAAAAAAA", "pattern": "AAAB"})
        ],
        max_visual_size=200,
        max_benchmark_size=10000,
        counters=["char_comparisons", "alignments"]
    ),
    "rabin_karp": AlgorithmMetadata(
        id="rabin_karp",
        name="Rabin-Karp Algorithm",
        category="String matching",
        compare_group="String matching",
        stage="string",
        description="Uses rolling hash to quickly filter out text positions that cannot match the pattern, checking character by character only on hash match.",
        complexity={
            "best": "O(n + m)",
            "average": "O(n + m)",
            "worst": "O(n * m)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="string",
            description="Text string and Pattern string.",
            fields={"text": "str", "pattern": "str"}
        ),
        presets=[
            PresetDef(name="match", label="Single Match", input={"text": "GEEKS FOR GEEKS", "pattern": "GEEK"}),
            PresetDef(name="multiple", label="Multiple Matches", input={"text": "AABAACAADAABAABA", "pattern": "AABA"})
        ],
        max_visual_size=200,
        max_benchmark_size=10000,
        counters=["char_comparisons", "hash_calculations", "hash_matches"]
    ),
    "kmp_search": AlgorithmMetadata(
        id="kmp_search",
        name="Knuth-Morris-Pratt (KMP)",
        category="String matching",
        compare_group="String matching",
        stage="string",
        description="Preprocesses the pattern to construct a Longest Prefix Suffix (LPS) table to avoid re-examining previously matched characters.",
        complexity={
            "best": "O(n)",
            "average": "O(n + m)",
            "worst": "O(n + m)",
            "space": "O(m)"
        },
        input_schema=InputSchemaDef(
            kind="string",
            description="Text string and Pattern string.",
            fields={"text": "str", "pattern": "str"}
        ),
        presets=[
            PresetDef(name="match", label="Single Match", input={"text": "ABABDABACDABABCABAB", "pattern": "ABABCABAB"}),
            PresetDef(name="multiple", label="Multiple Matches", input={"text": "ABACABABACAB", "pattern": "ABACAB"})
        ],
        max_visual_size=200,
        max_benchmark_size=10000,
        counters=["char_comparisons", "lps_lookups"]
    ),
    "z_search": AlgorithmMetadata(
        id="z_search",
        name="Z Algorithm",
        category="String matching",
        compare_group="String matching",
        stage="string",
        description="Constructs a Z-array for concatenated string (Pattern + '$' + Text) where Z[i] is the length of the longest common prefix starting at i.",
        complexity={
            "best": "O(n + m)",
            "average": "O(n + m)",
            "worst": "O(n + m)",
            "space": "O(n + m)"
        },
        input_schema=InputSchemaDef(
            kind="string",
            description="Text string and Pattern string.",
            fields={"text": "str", "pattern": "str"}
        ),
        presets=[
            PresetDef(name="match", label="Single Match", input={"text": "baabaa", "pattern": "aab"}),
            PresetDef(name="multiple", label="Multiple Matches", input={"text": "aabaacaadaabaaba", "pattern": "aaba"})
        ],
        max_visual_size=200,
        max_benchmark_size=10000,
        counters=["char_comparisons", "z_box_updates"]
    ),

    # --- DYNAMIC PROGRAMMING ---
    "knapsack_01": AlgorithmMetadata(
        id="knapsack_01",
        name="0/1 Knapsack Problem",
        category="Dynamic programming",
        compare_group=None,
        stage="dp",
        description="Determines the maximum total value of items that can be carried in a knapsack of capacity W, choosing to include or exclude each item.",
        complexity={
            "best": "O(n * W)",
            "average": "O(n * W)",
            "worst": "O(n * W)",
            "space": "O(n * W)"
        },
        input_schema=InputSchemaDef(
            kind="dp_knapsack",
            description="Weights, Values, and Capacity.",
            fields={"weights": "List[int]", "values": "List[int]", "capacity": "int"}
        ),
        presets=[
            PresetDef(name="normal", label="Standard Items", input={"weights": [2, 3, 4, 5], "values": [3, 4, 5, 6], "capacity": 5})
        ],
        max_visual_size=20,
        max_benchmark_size=1000,
        counters=["dp_updates", "comparisons"]
    ),
    "lcs": AlgorithmMetadata(
        id="lcs",
        name="Longest Common Subsequence",
        category="Dynamic programming",
        compare_group=None,
        stage="dp",
        description="Finds the length of the longest subsequence common to two sequences.",
        complexity={
            "best": "O(m * n)",
            "average": "O(m * n)",
            "worst": "O(m * n)",
            "space": "O(m * n)"
        },
        input_schema=InputSchemaDef(
            kind="dp_lcs",
            description="Two strings str1 and str2.",
            fields={"str1": "str", "str2": "str"}
        ),
        presets=[
            PresetDef(name="normal", label="Standard Strings", input={"str1": "AGGTAB", "str2": "GXTXAYB"})
        ],
        max_visual_size=20,
        max_benchmark_size=1000,
        counters=["dp_updates", "char_comparisons"]
    ),
    "lis": AlgorithmMetadata(
        id="lis",
        name="Longest Increasing Subsequence",
        category="Dynamic programming",
        compare_group=None,
        stage="dp",
        description="Finds the length of the longest subsequence of a given sequence such that all elements of the subsequence are sorted in increasing order.",
        complexity={
            "best": "O(n²)",
            "average": "O(n²)",
            "worst": "O(n²)",
            "space": "O(n)"
        },
        input_schema=InputSchemaDef(
            kind="dp_lis",
            description="Array of integers.",
            fields={"array": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Standard Array", input={"array": [10, 22, 9, 33, 21, 50, 41, 60, 80]})
        ],
        max_visual_size=30,
        max_benchmark_size=2000,
        counters=["dp_updates", "comparisons"]
    ),
    "mcm": AlgorithmMetadata(
        id="mcm",
        name="Matrix Chain Multiplication",
        category="Dynamic programming",
        compare_group=None,
        stage="dp",
        description="Determines the optimal parenthesization of a sequence of matrices to minimize scalar multiplications.",
        complexity={
            "best": "O(n³)",
            "average": "O(n³)",
            "worst": "O(n³)",
            "space": "O(n²)"
        },
        input_schema=InputSchemaDef(
            kind="dp_mcm",
            description="Array of matrix dimensions p, where matrix i has dimension p[i-1] x p[i].",
            fields={"dimensions": "List[int]"}
        ),
        presets=[
            PresetDef(name="normal", label="Standard Matrices", input={"dimensions": [10, 30, 5, 60]})
        ],
        max_visual_size=15,
        max_benchmark_size=500,
        counters=["dp_updates", "multiplications_calculated"]
    ),
    "edit_distance": AlgorithmMetadata(
        id="edit_distance",
        name="Edit Distance (Levenshtein)",
        category="Dynamic programming",
        compare_group=None,
        stage="dp",
        description="Computes the minimum number of single-character insertions, deletions, or substitutions required to change one string into another.",
        complexity={
            "best": "O(m * n)",
            "average": "O(m * n)",
            "worst": "O(m * n)",
            "space": "O(m * n)"
        },
        input_schema=InputSchemaDef(
            kind="dp_edit_distance",
            description="Source string and Target string.",
            fields={"str1": "str", "str2": "str"}
        ),
        presets=[
            PresetDef(name="normal", label="Standard Words", input={"str1": "kitten", "str2": "sitting"})
        ],
        max_visual_size=20,
        max_benchmark_size=1000,
        counters=["dp_updates", "comparisons"]
    ),

    # --- GRAPH ALGORITHMS ---
    "bfs": AlgorithmMetadata(
        id="bfs",
        name="Breadth-First Search (BFS)",
        category="Graph: traversal",
        compare_group="Traversal",
        stage="graph",
        description="Traverses a graph level by level starting from a source node using a queue.",
        complexity={
            "best": "O(V + E)",
            "average": "O(V + E)",
            "worst": "O(V + E)",
            "space": "O(V)"
        },
        input_schema=InputSchemaDef(
            kind="graph",
            description="Edge list string, start vertex, directed flag.",
            fields={"edges": "str", "start": "str", "directed": "bool"}
        ),
        presets=[
            PresetDef(name="normal", label="Sample Graph", input={"edges": "A B\nA C\nB D\nB E\nC F\nE F", "start": "A", "directed": False})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["node_visits", "edge_traversals"]
    ),
    "dfs": AlgorithmMetadata(
        id="dfs",
        name="Depth-First Search (DFS)",
        category="Graph: traversal",
        compare_group="Traversal",
        stage="graph",
        description="Traverses a graph by exploring as far as possible along each branch before backtracking using a stack/recursion.",
        complexity={
            "best": "O(V + E)",
            "average": "O(V + E)",
            "worst": "O(V + E)",
            "space": "O(V)"
        },
        input_schema=InputSchemaDef(
            kind="graph",
            description="Edge list string, start vertex, directed flag.",
            fields={"edges": "str", "start": "str", "directed": "bool"}
        ),
        presets=[
            PresetDef(name="normal", label="Sample Graph", input={"edges": "A B\nA C\nB D\nB E\nC F\nE F", "start": "A", "directed": False})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["node_visits", "edge_traversals"]
    ),
    "dijkstra": AlgorithmMetadata(
        id="dijkstra",
        name="Dijkstra's Algorithm",
        category="Graph: shortest paths",
        compare_group="Shortest path",
        stage="graph",
        description="Finds the shortest paths from a single source node to all other nodes in a graph with non-negative edge weights.",
        complexity={
            "best": "O((V + E) log V)",
            "average": "O((V + E) log V)",
            "worst": "O((V + E) log V)",
            "space": "O(V)"
        },
        input_schema=InputSchemaDef(
            kind="graph",
            description="Weighted edge list (A B 4), start vertex, directed flag.",
            fields={"edges": "str", "start": "str", "directed": "bool"}
        ),
        presets=[
            PresetDef(name="normal", label="Weighted Graph", input={"edges": "A B 4\nA C 2\nB C 1\nB D 5\nC D 8\nC E 10\nD E 2", "start": "A", "directed": False})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["node_visits", "edge_relaxations"]
    ),
    "bellman_ford": AlgorithmMetadata(
        id="bellman_ford",
        name="Bellman-Ford Algorithm",
        category="Graph: shortest paths",
        compare_group="Shortest path",
        stage="graph",
        description="Computes single-source shortest paths in a weighted graph, supporting negative edge weights and detecting negative cycles.",
        complexity={
            "best": "O(V * E)",
            "average": "O(V * E)",
            "worst": "O(V * E)",
            "space": "O(V)"
        },
        input_schema=InputSchemaDef(
            kind="graph",
            description="Weighted edge list (A B 4), start vertex, directed flag.",
            fields={"edges": "str", "start": "str", "directed": "bool"}
        ),
        presets=[
            PresetDef(name="normal", label="Weighted Graph", input={"edges": "A B 4\nA C 2\nB C -1\nB D 2\nC D 3", "start": "A", "directed": True})
        ],
        max_visual_size=50,
        max_benchmark_size=3000,
        counters=["iterations", "edge_relaxations"]
    ),
    "floyd_warshall": AlgorithmMetadata(
        id="floyd_warshall",
        name="Floyd-Warshall Algorithm",
        category="Graph: shortest paths",
        compare_group=None,
        stage="graph",
        description="Computes shortest paths between all pairs of vertices in a weighted graph.",
        complexity={
            "best": "O(V³)",
            "average": "O(V³)",
            "worst": "O(V³)",
            "space": "O(V²)"
        },
        input_schema=InputSchemaDef(
            kind="graph",
            description="Weighted edge list, directed flag.",
            fields={"edges": "str", "directed": "bool"}
        ),
        presets=[
            PresetDef(name="normal", label="Small Graph", input={"edges": "A B 3\nA C 8\nB C 1\nC A 4", "directed": True})
        ],
        max_visual_size=20,
        max_benchmark_size=500,
        counters=["triple_loops", "matrix_updates"]
    ),
    "prim": AlgorithmMetadata(
        id="prim",
        name="Prim's Algorithm",
        category="Graph: spanning trees",
        compare_group="Minimum spanning tree",
        stage="graph",
        description="Greedy algorithm that builds a minimum spanning tree for a weighted undirected graph by attaching the cheapest edge to the growing tree.",
        complexity={
            "best": "O((E + V) log V)",
            "average": "O((E + V) log V)",
            "worst": "O((E + V) log V)",
            "space": "O(V + E)"
        },
        input_schema=InputSchemaDef(
            kind="graph",
            description="Weighted edge list, start vertex.",
            fields={"edges": "str", "start": "str"}
        ),
        presets=[
            PresetDef(name="normal", label="MST Sample", input={"edges": "A B 4\nA C 8\nB C 11\nB D 8\nC E 7\nD E 2", "start": "A"})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["node_visits", "edge_evaluations"]
    ),
    "kruskal": AlgorithmMetadata(
        id="kruskal",
        name="Kruskal's Algorithm",
        category="Graph: spanning trees",
        compare_group="Minimum spanning tree",
        stage="graph",
        description="Finds a minimum spanning forest by sorting all edges by weight and adding them one by one if they don't form a cycle (using Disjoint-Set Union).",
        complexity={
            "best": "O(E log E)",
            "average": "O(E log E)",
            "worst": "O(E log E)",
            "space": "O(V + E)"
        },
        input_schema=InputSchemaDef(
            kind="graph",
            description="Weighted edge list.",
            fields={"edges": "str"}
        ),
        presets=[
            PresetDef(name="normal", label="MST Sample", input={"edges": "A B 4\nA C 8\nB C 11\nB D 8\nC E 7\nD E 2"})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["edge_evaluations", "union_find_ops"]
    ),

    # --- GREEDY ALGORITHMS ---
    "activity_selection": AlgorithmMetadata(
        id="activity_selection",
        name="Activity Selection",
        category="Greedy",
        compare_group=None,
        stage="greedy",
        description="Selects the maximum number of mutually compatible activities that can be performed by a single person or machine.",
        complexity={
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="greedy_activity",
            description="List of activities with start and finish times.",
            fields={"activities": "List[Dict[str, int]]"}
        ),
        presets=[
            PresetDef(name="normal", label="Standard Activities", input={"activities": [
                {"name": "a1", "start": 1, "finish": 4},
                {"name": "a2", "start": 3, "finish": 5},
                {"name": "a3", "start": 0, "finish": 6},
                {"name": "a4", "start": 5, "finish": 7},
                {"name": "a5", "start": 3, "finish": 9},
                {"name": "a6", "start": 5, "finish": 9},
                {"name": "a7", "start": 6, "finish": 10},
                {"name": "a8", "start": 8, "finish": 11},
                {"name": "a9", "start": 8, "finish": 12},
                {"name": "a10", "start": 2, "finish": 14},
                {"name": "a11", "start": 12, "finish": 14}
            ]})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["sort_ops", "greedy_selections", "rejections"]
    ),
    "fractional_knapsack": AlgorithmMetadata(
        id="fractional_knapsack",
        name="Fractional Knapsack",
        category="Greedy",
        compare_group=None,
        stage="greedy",
        description="Fills a knapsack of capacity W with items to maximize total value, allowing fractions of items to be taken.",
        complexity={
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(1)"
        },
        input_schema=InputSchemaDef(
            kind="greedy_knapsack",
            description="Items with weights and values, and capacity.",
            fields={"items": "List[Dict[str, float]]", "capacity": "float"}
        ),
        presets=[
            PresetDef(name="normal", label="Standard Items", input={
                "capacity": 50,
                "items": [
                    {"name": "Item 1", "weight": 10, "value": 60},
                    {"name": "Item 2", "weight": 20, "value": 100},
                    {"name": "Item 3", "weight": 30, "value": 120}
                ]
            })
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["ratio_calcs", "sort_ops", "greedy_selections"]
    ),
    "huffman_coding": AlgorithmMetadata(
        id="huffman_coding",
        name="Huffman Coding",
        category="Greedy",
        compare_group=None,
        stage="greedy",
        description="Constructs an optimal prefix tree for lossless data compression based on character frequencies.",
        complexity={
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(n)"
        },
        input_schema=InputSchemaDef(
            kind="greedy_huffman",
            description="Frequencies map or text string.",
            fields={"text": "str"}
        ),
        presets=[
            PresetDef(name="normal", label="Sample Text", input={"text": "abracadabra"})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["tree_merges", "priority_queue_ops"]
    ),
    "job_sequencing": AlgorithmMetadata(
        id="job_sequencing",
        name="Job Sequencing with Deadlines",
        category="Greedy",
        compare_group=None,
        stage="greedy",
        description="Schedules jobs each with a deadline and profit to maximize total profit, assuming each job takes 1 unit of time.",
        complexity={
            "best": "O(n²)",
            "average": "O(n²)",
            "worst": "O(n²)",
            "space": "O(n)"
        },
        input_schema=InputSchemaDef(
            kind="greedy_jobs",
            description="List of jobs with id, deadline, and profit.",
            fields={"jobs": "List[Dict[str, int]]"}
        ),
        presets=[
            PresetDef(name="normal", label="Sample Jobs", input={"jobs": [
                {"id": "j1", "deadline": 2, "profit": 100},
                {"id": "j2", "deadline": 1, "profit": 19},
                {"id": "j3", "deadline": 2, "profit": 27},
                {"id": "j4", "deadline": 1, "profit": 25},
                {"id": "j5", "deadline": 3, "profit": 15}
            ]})
        ],
        max_visual_size=50,
        max_benchmark_size=5000,
        counters=["sort_ops", "slot_searches", "greedy_selections"]
    )
}


def get_all_algorithms() -> List[AlgorithmMetadata]:
    return list(ALGORITHM_REGISTRY.values())


def get_algorithm(algorithm_id: str) -> Optional[AlgorithmMetadata]:
    return ALGORITHM_REGISTRY.get(algorithm_id)


def get_compare_groups() -> List[str]:
    groups = set()
    for meta in ALGORITHM_REGISTRY.values():
        if meta.compare_group:
            groups.add(meta.compare_group)
    return sorted(list(groups))
