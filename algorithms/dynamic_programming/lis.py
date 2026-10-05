from typing import Any, Dict, List, Tuple


def run_lis(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    n = len(arr)
    dp_updates = 0
    comparisons = 0

    if mode == "silent":
        dp = [1] * n
        parent = [-1] * n
        for i in range(1, n):
            for j in range(i):
                comparisons += 1
                if arr[i] > arr[j] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
                    dp_updates += 1

        max_len = max(dp) if n > 0 else 0
        best_idx = dp.index(max_len) if n > 0 else -1
        lis_seq = []
        curr = best_idx
        while curr != -1:
            lis_seq.append(arr[curr])
            curr = parent[curr]
        lis_seq.reverse()
        return {"output": max_len, "solution": lis_seq, "counters": {"dp_updates": dp_updates, "comparisons": comparisons}}

    def generator():
        nonlocal dp_updates, comparisons
        dp = [1] * n
        parent = [-1] * n
        row_labels = ["LIS DP"]
        col_labels = [f"idx {i} ({arr[i]})" for i in range(n)]

        yield {
            "type": "init",
            "message": f"Initializing LIS DP array of size {n}.",
            "state": {
                "table": [list(dp)],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [0, 0],
                "dependent_cells": [],
                "formula": "dp[i] = max LIS ending at index i"
            },
            "counters": {"dp_updates": 0, "comparisons": 0}
        }

        for i in range(1, n):
            for j in range(i):
                comparisons += 1
                is_greater = (arr[i] > arr[j])
                if is_greater and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
                    dp_updates += 1
                    formula_text = f"arr[{i}] ({arr[i]}) > arr[{j}] ({arr[j]}): dp[{i}] updated to {dp[i]}"
                else:
                    formula_text = f"Checking arr[{i}] ({arr[i]}) vs arr[{j}] ({arr[j]}): dp[{i}] remains {dp[i]}"

                yield {
                    "type": "cell_update",
                    "message": f"Comparing index {i} and {j}: {formula_text}.",
                    "state": {
                        "table": [list(dp)],
                        "row_labels": row_labels,
                        "col_labels": col_labels,
                        "current_cell": [0, i],
                        "dependent_cells": [[0, j]],
                        "formula": formula_text
                    },
                    "counters": {"dp_updates": 1 if (is_greater and dp[j] + 1 > dp[i]) else 0, "comparisons": 1}
                }

        max_len = max(dp) if n > 0 else 0
        best_idx = dp.index(max_len) if n > 0 else -1
        lis_seq = []
        path = []
        curr = best_idx
        while curr != -1:
            path.append([0, curr])
            lis_seq.append(arr[curr])
            curr = parent[curr]
        lis_seq.reverse()

        yield {
            "type": "done",
            "message": f"LIS complete. Max Length = {max_len}, Subsequence = {lis_seq}.",
            "state": {
                "table": [list(dp)],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [0, best_idx],
                "dependent_cells": [],
                "solution_path": path,
                "formula": f"Longest Increasing Subsequence: {lis_seq}"
            },
            "counters": {}
        }

    return generator(), None
