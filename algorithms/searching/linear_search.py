from typing import Any, Dict, List, Tuple


def run_linear_search(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    target = input_data["target"]
    n = len(arr)
    comparisons = 0
    iterations = 0
    found_idx = -1

    if mode == "silent":
        for i in range(n):
            comparisons += 1
            iterations += 1
            if arr[i] == target:
                found_idx = i
                break
        return {"output": found_idx, "solution": found_idx, "counters": {"comparisons": comparisons, "iterations": iterations}}

    def generator():
        nonlocal comparisons, iterations, found_idx
        yield {
            "type": "init",
            "message": f"Starting Linear Search for target {target} in array of size {n}.",
            "state": {
                "array": list(arr),
                "highlights": {},
                "pointers": {"target": target}
            },
            "counters": {"comparisons": 0, "iterations": 0}
        }

        for i in range(n):
            comparisons += 1
            iterations += 1
            yield {
                "type": "compare",
                "message": f"Checking index {i}: element {arr[i]} == target {target}?",
                "state": {
                    "array": list(arr),
                    "highlights": {i: "comparing"},
                    "pointers": {"current": i, "target": target}
                },
                "counters": {"comparisons": 1, "iterations": 1}
            }

            if arr[i] == target:
                found_idx = i
                yield {
                    "type": "found",
                    "message": f"Target {target} found at index {i}!",
                    "state": {
                        "array": list(arr),
                        "highlights": {i: "found"},
                        "pointers": {"found": i}
                    },
                    "counters": {}
                }
                break

        if found_idx == -1:
            yield {
                "type": "not_found",
                "message": f"Target {target} was not found in the array.",
                "state": {
                    "array": list(arr),
                    "highlights": {},
                    "pointers": {}
                },
                "counters": {}
            }

        yield {
            "type": "done",
            "message": "Linear Search complete.",
            "state": {
                "array": list(arr),
                "highlights": {found_idx: "found"} if found_idx != -1 else {},
                "pointers": {}
            },
            "counters": {}
        }

    return generator(), found_idx
