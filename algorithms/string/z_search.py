from typing import Any, Dict, List, Tuple


def run_z_search(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    text = str(input_data["text"])
    pattern = str(input_data["pattern"])
    concat = pattern + "$" + text
    total_len = len(concat)
    m = len(pattern)
    n = len(text)

    matches = []
    char_comparisons = 0
    z_box_updates = 0

    if mode == "silent":
        Z = [0] * total_len
        L = R = 0
        for i in range(1, total_len):
            if i > R:
                L = R = i
                while R < total_len and concat[R - L] == concat[R]:
                    char_comparisons += 1
                    R += 1
                char_comparisons += 1
                Z[i] = R - L
                R -= 1
                z_box_updates += 1
            else:
                k = i - L
                if Z[k] < R - i + 1:
                    Z[i] = Z[k]
                else:
                    L = i
                    while R < total_len and concat[R - L] == concat[R]:
                        char_comparisons += 1
                        R += 1
                    char_comparisons += 1
                    Z[i] = R - L
                    R -= 1
                    z_box_updates += 1
            if Z[i] == m:
                matches.append(i - m - 1)
        return {"output": matches, "solution": matches, "counters": {"char_comparisons": char_comparisons, "z_box_updates": z_box_updates}}

    def generator():
        nonlocal char_comparisons, z_box_updates
        found_matches = []
        Z = [0] * total_len
        L = R = 0

        yield {
            "type": "init",
            "message": f"Starting Z-Algorithm on concatenated string '{concat}' (Pattern + '$' + Text).",
            "state": {
                "text": text,
                "pattern": pattern,
                "concat": concat,
                "z_array": list(Z),
                "z_box": [L, R],
                "position": 0,
                "matches": []
            },
            "counters": {"char_comparisons": 0, "z_box_updates": 0}
        }

        for i in range(1, total_len):
            if i > R:
                L = R = i
                z_box_updates += 1
                while R < total_len and concat[R - L] == concat[R]:
                    char_comparisons += 1
                    R += 1
                char_comparisons += 1
                Z[i] = R - L
                R -= 1
            else:
                k = i - L
                if Z[k] < R - i + 1:
                    Z[i] = Z[k]
                else:
                    L = i
                    z_box_updates += 1
                    while R < total_len and concat[R - L] == concat[R]:
                        char_comparisons += 1
                        R += 1
                    char_comparisons += 1
                    Z[i] = R - L
                    R -= 1

            if Z[i] == m:
                text_match_idx = i - m - 1
                found_matches.append(text_match_idx)
                yield {
                    "type": "match_found",
                    "message": f"Z[{i}] == {m}: Match detected starting at text index {text_match_idx}!",
                    "state": {
                        "text": text,
                        "pattern": pattern,
                        "concat": concat,
                        "z_array": list(Z),
                        "z_box": [L, R],
                        "position": max(0, text_match_idx),
                        "matches": list(found_matches)
                    },
                    "counters": {"z_box_updates": 1, "char_comparisons": 1}
                }
            else:
                yield {
                    "type": "z_update",
                    "message": f"Z[{i}] calculated as {Z[i]} with active Z-box [{L}, {R}].",
                    "state": {
                        "text": text,
                        "pattern": pattern,
                        "concat": concat,
                        "z_array": list(Z),
                        "z_box": [L, R],
                        "position": max(0, i - m - 1),
                        "matches": list(found_matches)
                    },
                    "counters": {}
                }

        yield {
            "type": "done",
            "message": f"Z-Algorithm complete. Found {len(found_matches)} match(es).",
            "state": {
                "text": text,
                "pattern": pattern,
                "concat": concat,
                "z_array": list(Z),
                "z_box": [L, R],
                "position": max(0, n - m),
                "matches": list(found_matches)
            },
            "counters": {}
        }

    return generator(), matches
