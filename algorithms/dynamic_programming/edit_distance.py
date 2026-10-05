from typing import Any, Dict, List, Tuple


def run_edit_distance(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    s1 = str(input_data["str1"])
    s2 = str(input_data["str2"])
    m = len(s1)
    n = len(s2)
    dp_updates = 0
    comparisons = 0

    if mode == "silent":
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp_updates += 1
                comparisons += 1
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],      # Deletion
                                       dp[i][j - 1],      # Insertion
                                       dp[i - 1][j - 1])  # Substitution
        return {"output": dp[m][n], "solution": dp[m][n], "counters": {"dp_updates": dp_updates, "comparisons": comparisons}}

    def generator():
        nonlocal dp_updates, comparisons
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        row_labels = ["-"] + [s1[i] for i in range(m)]
        col_labels = ["-"] + [s2[j] for j in range(n)]

        yield {
            "type": "init",
            "message": f"Initializing Edit Distance DP table for '{s1}' -> '{s2}'.",
            "state": {
                "table": [list(row) for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [0, 0],
                "dependent_cells": [],
                "formula": "dp[i][j] = min edits to transform s1[0..i-1] to s2[0..j-1]"
            },
            "counters": {"dp_updates": 0, "comparisons": 0}
        }

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp_updates += 1
                comparisons += 1
                is_match = (s1[i - 1] == s2[j - 1])

                if is_match:
                    dp[i][j] = dp[i - 1][j - 1]
                    formula_text = f"s1[{i-1}] ('{s1[i-1]}') == s2[{j-1}] ('{s2[j-1]}'): copy dp[{i-1}][{j-1}] -> {dp[i][j]}"
                    deps = [[i - 1, j - 1]]
                else:
                    delete_op = dp[i - 1][j]
                    insert_op = dp[i][j - 1]
                    replace_op = dp[i - 1][j - 1]
                    dp[i][j] = 1 + min(delete_op, insert_op, replace_op)
                    formula_text = f"1 + min(del={delete_op}, ins={insert_op}, rep={replace_op}) -> {dp[i][j]}"
                    deps = [[i - 1, j], [i, j - 1], [i - 1, j - 1]]

                yield {
                    "type": "cell_update",
                    "message": f"Updating dp[{i}][{j}]: {formula_text}.",
                    "state": {
                        "table": [list(row) for row in dp],
                        "row_labels": row_labels,
                        "col_labels": col_labels,
                        "current_cell": [i, j],
                        "dependent_cells": deps,
                        "formula": formula_text
                    },
                    "counters": {"dp_updates": 1, "comparisons": 1}
                }

        yield {
            "type": "done",
            "message": f"Edit Distance complete. Min operations required = {dp[m][n]}.",
            "state": {
                "table": [list(row) for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [m, n],
                "dependent_cells": [],
                "formula": f"Edit Distance = {dp[m][n]}"
            },
            "counters": {}
        }

    return generator(), None
