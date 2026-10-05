from typing import Any, Dict, List, Tuple


def run_naive_search(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    text = str(input_data["text"])
    pattern = str(input_data["pattern"])
    n = len(text)
    m = len(pattern)

    matches = []
    char_comparisons = 0
    alignments = 0

    if mode == "silent":
        for i in range(n - m + 1):
            alignments += 1
            j = 0
            while j < m:
                char_comparisons += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1
            if j == m:
                matches.append(i)
        return {"output": matches, "solution": matches, "counters": {"char_comparisons": char_comparisons, "alignments": alignments}}

    def generator():
        nonlocal char_comparisons, alignments
        found_matches = []

        yield {
            "type": "init",
            "message": f"Starting Naive String Matching for text (len {n}) and pattern '{pattern}' (len {m}).",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": 0,
                "char_states": {},
                "matches": []
            },
            "counters": {"char_comparisons": 0, "alignments": 0}
        }

        for i in range(n - m + 1):
            alignments += 1
            yield {
                "type": "align",
                "message": f"Aligning pattern at text index {i}.",
                "state": {
                    "text": text,
                    "pattern": pattern,
                    "position": i,
                    "char_states": {},
                    "matches": list(found_matches)
                },
                "counters": {"alignments": 1}
            }

            j = 0
            match_ok = True
            while j < m:
                char_comparisons += 1
                is_match = (text[i + j] == pattern[j])

                yield {
                    "type": "compare_char",
                    "message": f"Comparing text[{i+j}] ('{text[i+j]}') with pattern[{j}] ('{pattern[j]}').",
                    "state": {
                        "text": text,
                        "pattern": pattern,
                        "position": i,
                        "text_index": i + j,
                        "pattern_index": j,
                        "char_states": {
                            "text_index": i + j,
                            "pattern_index": j,
                            "status": "match" if is_match else "mismatch"
                        },
                        "matches": list(found_matches)
                    },
                    "counters": {"char_comparisons": 1}
                }

                if not is_match:
                    match_ok = False
                    break
                j += 1

            if match_ok and j == m:
                found_matches.append(i)
                yield {
                    "type": "match_found",
                    "message": f"Full pattern match found starting at text index {i}!",
                    "state": {
                        "text": text,
                        "pattern": pattern,
                        "position": i,
                        "char_states": {},
                        "matches": list(found_matches)
                    },
                    "counters": {}
                }

        yield {
            "type": "done",
            "message": f"Naive search completed. Found {len(found_matches)} match(es) at indices {found_matches}.",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": n - m if n >= m else 0,
                "char_states": {},
                "matches": list(found_matches)
            },
            "counters": {}
        }

    return generator(), matches