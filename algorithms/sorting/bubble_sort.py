from typing import Any, Dict, Generator, Tuple, List


def run_bubble_sort(input_data: Dict[str, Any], mode: str = "record") -> Tuple[List[int], List[int], Dict[str, int]]:
    arr = list(input_data["array"])
    n = len(arr)
    comparisons = 0
    swaps = 0
    iterations = 0

    if mode == "silent":
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
                    swapped = True
            iterations += 1
            if not swapped:
                break
        return {"output": arr, "solution": arr, "counters": {"comparisons": comparisons, "swaps": swaps, "iterations": iterations}}

    # Recording mode generator
    def generator():
        nonlocal comparisons, swaps, iterations
        work_arr = list(arr)
        sorted_indices = set()

        yield {
            "type": "init",
            "message": f"Starting Bubble Sort on array of size {n}.",
            "state": {
                "array": list(work_arr),
                "highlights": {},
                "pointers": {},
                "sorted_indices": []
            },
            "counters": {"comparisons": 0, "swaps": 0, "iterations": 0}
        }

        for i in range(n):
            swapped = False
            iterations += 1
            for j in range(0, n - i - 1):
                comparisons += 1
                # Comparison step
                yield {
                    "type": "compare",
                    "message": f"Comparing elements at index {j} ({work_arr[j]}) and index {j+1} ({work_arr[j+1]}).",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {j: "comparing", j + 1: "comparing"},
                        "pointers": {"current": j},
                        "sorted_indices": sorted(list(sorted_indices))
                    },
                    "counters": {"comparisons": 1}
                }

                if work_arr[j] > work_arr[j + 1]:
                    work_arr[j], work_arr[j + 1] = work_arr[j + 1], work_arr[j]
                    swaps += 1
                    swapped = True
                    # Swap step
                    yield {
                        "type": "swap",
                        "message": f"Swapped {work_arr[j+1]} and {work_arr[j]} at indices {j} and {j+1}.",
                        "state": {
                            "array": list(work_arr),
                            "highlights": {j: "swapping", j + 1: "swapping"},
                            "pointers": {"current": j + 1},
                            "sorted_indices": sorted(list(sorted_indices))
                        },
                        "counters": {"swaps": 1}
                    }

            sorted_indices.add(n - i - 1)
            yield {
                "type": "pass_done",
                "message": f"Pass {i+1} complete. Element at index {n-i-1} ({work_arr[n-i-1]}) is now sorted.",
                "state": {
                    "array": list(work_arr),
                    "highlights": {n - i - 1: "sorted"},
                    "pointers": {},
                    "sorted_indices": sorted(list(sorted_indices))
                },
                "counters": {"iterations": 1}
            }

            if not swapped:
                for idx in range(n):
                    sorted_indices.add(idx)
                break

        yield {
            "type": "done",
            "message": "Bubble Sort finished. Array is fully sorted.",
            "state": {
                "array": list(work_arr),
                "highlights": {idx: "sorted" for idx in range(n)},
                "pointers": {},
                "sorted_indices": list(range(n))
            },
            "counters": {}
        }

    return generator(), arr
