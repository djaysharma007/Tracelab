from typing import Any, Dict, List, Tuple


def run_insertion_sort(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    n = len(arr)
    comparisons = 0
    shifts = 0
    iterations = 0

    if mode == "silent":
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            iterations += 1
            while j >= 0 and arr[j] > key:
                comparisons += 1
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            if j >= 0:
                comparisons += 1
            arr[j + 1] = key
        return {"output": arr, "solution": arr, "counters": {"comparisons": comparisons, "shifts": shifts, "iterations": iterations}}

    def generator():
        nonlocal comparisons, shifts, iterations
        work_arr = list(arr)

        yield {
            "type": "init",
            "message": f"Starting Insertion Sort on array of size {n}.",
            "state": {
                "array": list(work_arr),
                "highlights": {0: "sorted"},
                "pointers": {},
                "sorted_indices": [0]
            },
            "counters": {"comparisons": 0, "shifts": 0, "iterations": 0}
        }

        for i in range(1, n):
            key = work_arr[i]
            j = i - 1
            iterations += 1

            yield {
                "type": "select_key",
                "message": f"Selecting element at index {i} ({key}) as key to insert into sorted sub-array [0..{i-1}].",
                "state": {
                    "array": list(work_arr),
                    "highlights": {i: "pointer"},
                    "pointers": {"key": i},
                    "sorted_indices": list(range(i))
                },
                "counters": {"iterations": 1}
            }

            while j >= 0 and work_arr[j] > key:
                comparisons += 1
                yield {
                    "type": "compare",
                    "message": f"Comparing key ({key}) with element at index {j} ({work_arr[j]}).",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {j: "comparing", j + 1: "pointer"},
                        "pointers": {"key_val": key, "compare": j},
                        "sorted_indices": list(range(i))
                    },
                    "counters": {"comparisons": 1}
                }

                work_arr[j + 1] = work_arr[j]
                shifts += 1
                yield {
                    "type": "shift",
                    "message": f"Shifted element {work_arr[j]} from index {j} to index {j+1}.",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {j + 1: "swapping"},
                        "pointers": {"key_val": key, "compare": j},
                        "sorted_indices": list(range(i))
                    },
                    "counters": {"shifts": 1}
                }
                j -= 1

            if j >= 0:
                comparisons += 1

            work_arr[j + 1] = key
            yield {
                "type": "insert",
                "message": f"Inserted key ({key}) into position at index {j+1}.",
                "state": {
                    "array": list(work_arr),
                    "highlights": {j + 1: "sorted"},
                    "pointers": {},
                    "sorted_indices": list(range(i + 1))
                },
                "counters": {}
            }

        yield {
            "type": "done",
            "message": "Insertion Sort finished. Array is fully sorted.",
            "state": {
                "array": list(work_arr),
                "highlights": {idx: "sorted" for idx in range(n)},
                "pointers": {},
                "sorted_indices": list(range(n))
            },
            "counters": {}
        }

    return generator(), arr
