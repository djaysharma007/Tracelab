from typing import Any, Dict, List, Tuple


def run_knapsack_01(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    weights = list(input_data["weights"])
    values = list(input_data["values"])
    capacity = int(input_data["capacity"])
    n = len(weights)
    dp_updates = 0
    comparisons = 0

    if mode == "silent":
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            w = weights[i - 1]
            v = values[i - 1]
            for c in range(capacity + 1):
                dp_updates += 1
                if w <= c:
                    comparisons += 1
                    dp[i][c] = max(dp[i - 1][c], v + dp[i - 1][c - w])
                else:
                    dp[i][c] = dp[i - 1][c]

        # Reconstruct solution
        selected_items = []
        c = capacity
        for i in range(n, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                selected_items.append(i - 1)
                c -= weights[i - 1]
        selected_items.reverse()
        return {"output": dp[n][capacity], "solution": selected_items, "counters": {"dp_updates": dp_updates, "comparisons": comparisons}}

    def generator():
        nonlocal dp_updates, comparisons
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        row_labels = ["0 (Empty)"] + [f"Item {i+1} (w={weights[i]}, v={values[i]})" for i in range(n)]
        col_labels = [str(c) for c in range(capacity + 1)]

        yield {
            "type": "init",
            "message": f"Initializing 0/1 Knapsack DP table of size ({n+1} x {capacity+1}).",
            "state": {
                "table": [list(row) for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [0, 0],
                "dependent_cells": [],
                "formula": "dp[i][c] = max value with first i items and capacity c"
            },
            "counters": {"dp_updates": 0, "comparisons": 0}
        }

        for i in range(1, n + 1):
            w = weights[i - 1]
            v = values[i - 1]
            for c in range(capacity + 1):
                dp_updates += 1
                if w <= c:
                    comparisons += 1
                    take = v + dp[i - 1][c - w]
                    skip = dp[i - 1][c]
                    dp[i][c] = max(skip, take)
                    formula_text = f"max(skip={skip}, take={v}+{dp[i-1][c-w]}={take}) -> {dp[i][c]}"
                    deps = [[i - 1, c], [i - 1, c - w]]
                else:
                    dp[i][c] = dp[i - 1][c]
                    formula_text = f"Weight {w} > capacity {c}; skip item -> {dp[i][c]}"
                    deps = [[i - 1, c]]

                yield {
                    "type": "cell_update",
                    "message": f"Updating dp[{i}][{c}]: {formula_text}.",
                    "state": {
                        "table": [list(row) for row in dp],
                        "row_labels": row_labels,
                        "col_labels": col_labels,
                        "current_cell": [i, c],
                        "dependent_cells": deps,
                        "formula": formula_text
                    },
                    "counters": {"dp_updates": 1, "comparisons": 1 if w <= c else 0}
                }

        # Backtrack solution
        selected_items = []
        path = []
        c_curr = capacity
        for i in range(n, 0, -1):
            path.append([i, c_curr])
            if dp[i][c_curr] != dp[i - 1][c_curr]:
                selected_items.append(i - 1)
                c_curr -= weights[i - 1]
        path.append([0, c_curr])
        selected_items.reverse()

        yield {
            "type": "done",
            "message": f"0/1 Knapsack complete. Max Value = {dp[n][capacity]}, Selected Items = {selected_items}.",
            "state": {
                "table": [list(row) for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [n, capacity],
                "dependent_cells": [],
                "solution_path": path,
                "formula": f"Optimal Solution: Max Value {dp[n][capacity]}"
            },
            "counters": {}
        }

    return generator(), None
