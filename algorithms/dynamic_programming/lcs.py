from typing import Any, Dict, List, Tuple


def run_lcs(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    s1 = str(input_data["str1"])
    s2 = str(input_data["str2"])
    m = len(s1)
    n = len(s2)
    dp_updates = 0
    char_comparisons = 0

    if mode == "silent":
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp_updates += 1
                char_comparisons += 1
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Backtrack
        lcs_chars = []
        i, j = m, n
        while i > 0 and j > 0:
            if s1[i - 1] == s2[j - 1]:
                lps_char = s1[i - 1]
                lcs_chars.append(lps_char)
                i -= 1
                j -= 1
            elif dp[i - 1][j] >= dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        lcs_str = "".join(reversed(lcs_chars))
        return {"output": dp[m][n], "solution": lcs_str, "counters": {"dp_updates": dp_updates, "char_comparisons": char_comparisons}}

    def generator():
        nonlocal dp_updates, char_comparisons
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        row_labels = ["-"] + [s1[i] for i in range(m)]
        col_labels = ["-"] + [s2[j] for j in range(n)]

        yield {
            "type": "init",
            "message": f"Initializing LCS DP table of size ({m+1} x {n+1}) for '{s1}' and '{s2}'.",
            "state": {
                "table": [list(row) for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [0, 0],
                "dependent_cells": [],
                "formula": "dp[i][j] = LCS length for s1[0..i-1] and s2[0..j-1]"
            },
            "counters": {"dp_updates": 0, "char_comparisons": 0}
        }

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp_updates += 1
                char_comparisons += 1
                is_match = (s1[i - 1] == s2[j - 1])

                if is_match:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    formula_text = f"s1[{i-1}] ('{s1[i-1]}') == s2[{j-1}] ('{s2[j-1]}'): 1 + dp[{i-1}][{j-1}] -> {dp[i][j]}"
                    deps = [[i - 1, j - 1]]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                    formula_text = f"s1[{i-1}] != s2[{j-1}]: max(dp[{i-1}][{j}], dp[{i}][{j-1}]) -> {dp[i][j]}"
                    deps = [[i - 1, j], [i, j - 1]]

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
                    "counters": {"dp_updates": 1, "char_comparisons": 1}
                }

        # Backtrack solution string
        lcs_chars = []
        path = []
        curr_i, curr_j = m, n
        while curr_i > 0 and curr_j > 0:
            path.append([curr_i, curr_j])
            if s1[curr_i - 1] == s2[curr_j - 1]:
                lcs_chars.append(s1[curr_i - 1])
                curr_i -= 1
                curr_j -= 1
            elif dp[curr_i - 1][curr_j] >= dp[curr_i][curr_j - 1]:
                curr_i -= 1
            else:
                curr_j -= 1
        path.append([curr_i, curr_j])
        lcs_str = "".join(reversed(lcs_chars))

        yield {
            "type": "done",
            "message": f"LCS complete. Length = {dp[m][n]}, Subsequence = '{lcs_str}'.",
            "state": {
                "table": [list(row) for row in dp],
                "row_labels": row_labels,
                "col_labels": col_labels,
                "current_cell": [m, n],
                "dependent_cells": [],
                "solution_path": path,
                "formula": f"Longest Common Subsequence: '{lcs_str}'"
            },
            "counters": {}
        }

    return generator(), None
