from typing import Any, Dict, List, Tuple


def run_binary_search(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    target = input_data["target"]
    n = len(arr)
    comparisons = 0
    iterations = 0
    found_idx = -1

    if mode == "silent":
        low = 0
        high = n - 1
        while low <= high:
            iterations += 1
            mid = (low + high) // 2
            comparisons += 1
            if arr[mid] == target:
                found_idx = mid
                break
            elif arr[mid] < target:
                comparisons += 1
                low = mid + 1
            else:
                comparisons += 1
                high = mid - 1
        return {"output": found_idx, "solution": found_idx, "counters": {"comparisons": comparisons, "iterations": iterations}}

    def generator():
        nonlocal comparisons, iterations, found_idx
        low = 0
        high = n - 1

        yield {
            "type": "init",
            "message": f"Starting Binary Search for target {target} in sorted array of size {n}.",
            "state": {
                "array": list(arr),
                "highlights": {},
                "pointers": {"low": low, "high": high, "target": target}
            },
            "counters": {"comparisons": 0, "iterations": 0}
        }

        while low <= high:
            iterations += 1
            mid = (low + high) // 2

            yield {
                "type": "inspect_mid",
                "message": f"Range [{low}..{high}]: calculated mid = {mid} (element {arr[mid]}).",
                "state": {
                    "array": list(arr),
                    "highlights": {mid: "pointer", low: "pointer", high: "pointer"},
                    "pointers": {"low": low, "mid": mid, "high": high, "target": target}
                },
                "counters": {"iterations": 1}
            }

            comparisons += 1
            if arr[mid] == target:
                found_idx = mid
                yield {
                    "type": "found",
                    "message": f"Target {target} found at index {mid}!",
                    "state": {
                        "array": list(arr),
                        "highlights": {mid: "found"},
                        "pointers": {"found": mid}
                    },
                    "counters": {"comparisons": 1}
                }
                break

            elif arr[mid] < target:
                comparisons += 1
                yield {
                    "type": "compare",
                    "message": f"arr[{mid}] ({arr[mid]}) < target ({target}). Target is in right half. Adjusting low = {mid+1}.",
                    "state": {
                        "array": list(arr),
                        "highlights": {mid: "comparing"},
                        "pointers": {"low": mid + 1, "high": high, "target": target}
                    },
                    "counters": {"comparisons": 2}
                }
                low = mid + 1
            else:
                comparisons += 1
                yield {
                    "type": "compare",
                    "message": f"arr[{mid}] ({arr[mid]}) > target ({target}). Target is in left half. Adjusting high = {mid-1}.",
                    "state": {
                        "array": list(arr),
                        "highlights": {mid: "comparing"},
                        "pointers": {"low": low, "high": mid - 1, "target": target}
                    },
                    "counters": {"comparisons": 2}
                }
                high = mid - 1

        if found_idx == -1:
            yield {
                "type": "not_found",
                "message": f"Target {target} is not in the array.",
                "state": {
                    "array": list(arr),
                    "highlights": {},
                    "pointers": {}
                },
                "counters": {}
            }

        yield {
            "type": "done",
            "message": "Binary Search complete.",
            "state": {
                "array": list(arr),
                "highlights": {found_idx: "found"} if found_idx != -1 else {},
                "pointers": {}
            },
            "counters": {}
        }

    return generator(), found_idx
