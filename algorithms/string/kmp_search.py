from typing import Any, Dict, List, Tuple


def run_kmp_search(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    text = str(input_data["text"])
    pattern = str(input_data["pattern"])
    n = len(text)
    m = len(pattern)

    matches = []
    char_comparisons = 0
    lps_lookups = 0

    if mode == "silent":
        if m > 0 and m <= n:
            lps = [0] * m
            length = 0
            i = 1
            while i < m:
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1

            i = 0
            j = 0
            while i < n:
                char_comparisons += 1
                if pattern[j] == text[i]:
                    i += 1
                    j += 1
                if j == m:
                    matches.append(i - j)
                    j = lps[j - 1]
                    lps_lookups += 1
                elif i < n and pattern[j] != text[i]:
                    if j != 0:
                        j = lps[j - 1]
                        lps_lookups += 1
                    else:
                        i += 1
        return {"output": matches, "solution": matches, "counters": {"char_comparisons": char_comparisons, "lps_lookups": lps_lookups}}

    def generator():
        nonlocal char_comparisons, lps_lookups
        found_matches = []
        lps = [0] * m

        yield {
            "type": "init",
            "message": f"Starting KMP Search for text (len {n}) and pattern '{pattern}' (len {m}).",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": 0,
                "lps": list(lps),
                "matches": []
            },
            "counters": {"char_comparisons": 0, "lps_lookups": 0}
        }

        # Build LPS array
        length = 0
        i_lps = 1
        while i_lps < m:
            if pattern[i_lps] == pattern[length]:
                length += 1
                lps[i_lps] = length
                i_lps += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i_lps] = 0
                    i_lps += 1

        yield {
            "type": "lps_built",
            "message": f"Constructed LPS (Longest Prefix Suffix) array: {lps}.",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": 0,
                "lps": list(lps),
                "matches": []
            },
            "counters": {}
        }

        i = 0  # text pointer
        j = 0  # pattern pointer
        while i < n:
            char_comparisons += 1
            is_match = (pattern[j] == text[i])

            yield {
                "type": "compare",
                "message": f"Comparing text[{i}] ('{text[i]}') and pattern[{j}] ('{pattern[j]}').",
                "state": {
                    "text": text,
                    "pattern": pattern,
                    "position": i - j,
                    "text_index": i,
                    "pattern_index": j,
                    "lps": list(lps),
                    "char_states": {
                        "text_index": i,
                        "pattern_index": j,
                        "status": "match" if is_match else "mismatch"
                    },
                    "matches": list(found_matches)
                },
                "counters": {"char_comparisons": 1}
            }

            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == m:
                found_matches.append(i - j)
                yield {
                    "type": "match_found",
                    "message": f"KMP Match found at text index {i - j}!",
                    "state": {
                        "text": text,
                        "pattern": pattern,
                        "position": i - j,
                        "lps": list(lps),
                        "matches": list(found_matches)
                    },
                    "counters": {}
                }
                j = lps[j - 1]
                lps_lookups += 1
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                    lps_lookups += 1
                    yield {
                        "type": "fallback",
                        "message": f"Mismatch! Using LPS table to shift pattern pointer j to {j}.",
                        "state": {
                            "text": text,
                            "pattern": pattern,
                            "position": i - j,
                            "text_index": i,
                            "pattern_index": j,
                            "lps": list(lps),
                            "matches": list(found_matches)
                        },
                        "counters": {"lps_lookups": 1}
                    }
                else:
                    i += 1

        yield {
            "type": "done",
            "message": f"KMP complete. Found {len(found_matches)} match(es).",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": max(0, n - m),
                "lps": list(lps),
                "matches": list(found_matches)
            },
            "counters": {}
        }

    return generator(), matches
