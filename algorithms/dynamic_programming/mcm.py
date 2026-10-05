from typing import Any, Dict, List, Tuple


def run_mcm(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    p = list(input_data["dimensions"])
    n = len(p) - 1
    dp_updates = 0
    multiplications_calculated = 0

    if mode == "silent":
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        for length in range(2, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                dp[i][j] = float('inf')
                for k in range(i, j):
                    multiplications_calculated += 1
                    q = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j]
                    if q < dp[i][j]:
                        dp[i][j] = q
                        dp_updates += 1
        return {"output": dp[1][n], "solution": dp[1][n], "counters": {"dp_updates": dp_updates, "multiplications_calculated": multiplications_calculated}}

    def generator():
        nonlocal dp_updates, multiplications_calculated
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        row_labels = [f"M{i}" for i in range(n + 1)]
        col_labels = [f"M{j}" for j in range(n + 1)]

        yield {
            "type": "init",
            "message": f"Initializing MCM DP matrix for {n} matrices with dimensions {p}.",
            "state": {
                "table": [list(row) for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [1, 1],
                "dependent_cells": [],
                "formula": "dp[i][j] = min scalar multiplications to multiply matrices i through j"
            },
            "counters": {"dp_updates": 0, "multiplications_calculated": 0}
        }

        for length in range(2, n + 1):
            for i in range(1, n - length + 2):
                j = i + length - 1
                dp[i][j] = float('inf')
                best_k = i
                for k in range(i, j):
                    multiplications_calculated += 1
                    cost = p[i - 1] * p[k] * p[j]
                    q = dp[i][k] + dp[k + 1][j] + cost
                    if q < dp[i][j]:
                        dp[i][j] = q
                        best_k = k
                        dp_updates += 1

                    formula_text = f"k={k}: dp[{i}][{k}]({dp[i][k]}) + dp[{k+1}][{j}]({dp[k+1][j]}) + {p[i-1]}*{p[k]}*{p[j]}({cost}) = {q}"

                    yield {
                        "type": "cell_update",
                        "message": f"Computing min multiplications for chain M[{i}..{j}] split at k={k}: {formula_text}.",
                        "state": {
                            "table": [[val if val != float('inf') else 0 for val in row] for row in dp],
                            "row_labels": row_labels,
                            "col_labels": col_labels,
                            "current_cell": [i, j],
                            "dependent_cells": [[i, k], [k + 1, j]],
                            "formula": formula_text
                        },
                        "counters": {"dp_updates": 1 if q < dp[i][j] else 0, "multiplications_calculated": 1}
                    }

        yield {
            "type": "done",
            "message": f"MCM complete. Min Scalar Multiplications = {dp[1][n]}.",
            "state": {
                "table": [[val if val != float('inf') else 0 for val in row] for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [1, n],
                "dependent_cells": [],
                "formula": f"Min Multiplications: {dp[1][n]}"
            },
            "counters": {}
        }

    return generator(), None
