from typing import Any, Dict, List, Tuple


def run_selection_sort(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    n = len(arr)
    comparisons = 0
    swaps = 0
    iterations = 0

    if mode == "silent":
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                comparisons += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swaps += 1
            iterations += 1
        return {"output": arr, "solution": arr, "counters": {"comparisons": comparisons, "swaps": swaps, "iterations": iterations}}

    def generator():
        nonlocal comparisons, swaps, iterations
        work_arr = list(arr)
        sorted_indices = set()

        yield {
            "type": "init",
            "message": f"Starting Selection Sort on array of size {n}.",
            "state": {
                "array": list(work_arr),
                "highlights": {},
                "pointers": {},
                "sorted_indices": []
            },
            "counters": {"comparisons": 0, "swaps": 0, "iterations": 0}
        }

        for i in range(n):
            min_idx = i
            iterations += 1

            yield {
                "type": "select_min",
                "message": f"Assume index {i} ({work_arr[i]}) is the current minimum for pass {i+1}.",
                "state": {
                    "array": list(work_arr),
                    "highlights": {i: "pointer"},
                    "pointers": {"min": min_idx, "pass": i},
                    "sorted_indices": sorted(list(sorted_indices))
                },
                "counters": {"iterations": 1}
            }

            for j in range(i + 1, n):
                comparisons += 1
                yield {
                    "type": "compare",
                    "message": f"Comparing element at index {j} ({work_arr[j]}) with current min at index {min_idx} ({work_arr[min_idx]}).",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {j: "comparing", min_idx: "pointer"},
                        "pointers": {"current": j, "min": min_idx},
                        "sorted_indices": sorted(list(sorted_indices))
                    },
                    "counters": {"comparisons": 1}
                }

                if work_arr[j] < work_arr[min_idx]:
                    min_idx = j
                    yield {
                        "type": "new_min",
                        "message": f"Found new minimum {work_arr[min_idx]} at index {min_idx}.",
                        "state": {
                            "array": list(work_arr),
                            "highlights": {min_idx: "pointer"},
                            "pointers": {"min": min_idx},
                            "sorted_indices": sorted(list(sorted_indices))
                        },
                        "counters": {}
                    }

            if min_idx != i:
                work_arr[i], work_arr[min_idx] = work_arr[min_idx], work_arr[i]
                swaps += 1
                yield {
                    "type": "swap",
                    "message": f"Swapping minimum element {work_arr[i]} into position index {i}.",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {i: "swapping", min_idx: "swapping"},
                        "pointers": {"min": i},
                        "sorted_indices": sorted(list(sorted_indices))
                    },
                    "counters": {"swaps": 1}
                }

            sorted_indices.add(i)

        yield {
            "type": "done",
            "message": "Selection Sort finished. Array is fully sorted.",
            "state": {
                "array": list(work_arr),
                "highlights": {idx: "sorted" for idx in range(n)},
                "pointers": {},
                "sorted_indices": list(range(n))
            },
            "counters": {}
        }

    return generator(), arr
