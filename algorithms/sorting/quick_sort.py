from typing import Any, Dict, List, Tuple


def run_quick_sort(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    n = len(arr)
    comparisons = 0
    swaps = 0
    recursive_calls = 0

    if mode == "silent":
        def silent_quick_sort(a, low, high):
            nonlocal comparisons, swaps, recursive_calls
            if low < high:
                pivot = a[high]
                i = low - 1
                for j in range(low, high):
                    comparisons += 1
                    if a[j] <= pivot:
                        i += 1
                        a[i], a[j] = a[j], a[i]
                        swaps += 1
                a[i + 1], a[high] = a[high], a[i + 1]
                swaps += 1
                pi = i + 1
                recursive_calls += 2
                silent_quick_sort(a, low, pi - 1)
                silent_quick_sort(a, pi + 1, high)

        work = list(arr)
        silent_quick_sort(work, 0, n - 1)
        return {"output": work, "solution": work, "counters": {"comparisons": comparisons, "swaps": swaps, "recursive_calls": recursive_calls}}

    def generator():
        nonlocal comparisons, swaps, recursive_calls
        work_arr = list(arr)
        sorted_indices = set()

        yield {
            "type": "init",
            "message": f"Starting Quick Sort on array of size {n}.",
            "state": {
                "array": list(work_arr),
                "highlights": {},
                "pointers": {},
                "sorted_indices": []
            },
            "counters": {"comparisons": 0, "swaps": 0, "recursive_calls": 0}
        }

        def quick_sort_rec(low, high):
            nonlocal comparisons, swaps, recursive_calls
            if low > high:
                return
            if low == high:
                sorted_indices.add(low)
                return

            pivot_val = work_arr[high]
            yield {
                "type": "select_pivot",
                "message": f"Partitioning sub-array [{low}..{high}] with pivot = {pivot_val} at index {high}.",
                "state": {
                    "array": list(work_arr),
                    "highlights": {high: "pivot"},
                    "pointers": {"pivot": high, "low": low, "high": high},
                    "sorted_indices": sorted(list(sorted_indices))
                },
                "counters": {}
            }

            i = low - 1
            for j in range(low, high):
                comparisons += 1
                yield {
                    "type": "compare",
                    "message": f"Comparing element at index {j} ({work_arr[j]}) with pivot ({pivot_val}).",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {j: "comparing", high: "pivot"},
                        "pointers": {"i": i if i >= low else low, "j": j, "pivot": high},
                        "sorted_indices": sorted(list(sorted_indices))
                    },
                    "counters": {"comparisons": 1}
                }

                if work_arr[j] <= pivot_val:
                    i += 1
                    if i != j:
                        work_arr[i], work_arr[j] = work_arr[j], work_arr[i]
                        swaps += 1
                        yield {
                            "type": "swap",
                            "message": f"Swapped {work_arr[j]} and {work_arr[i]} into smaller partition.",
                            "state": {
                                "array": list(work_arr),
                                "highlights": {i: "swapping", j: "swapping", high: "pivot"},
                                "pointers": {"i": i, "j": j, "pivot": high},
                                "sorted_indices": sorted(list(sorted_indices))
                            },
                            "counters": {"swaps": 1}
                        }

            work_arr[i + 1], work_arr[high] = work_arr[high], work_arr[i + 1]
            swaps += 1
            pi = i + 1
            sorted_indices.add(pi)

            yield {
                "type": "partition_done",
                "message": f"Pivot {pivot_val} placed at index {pi}. Left: [{low}..{pi-1}], Right: [{pi+1}..{high}].",
                "state": {
                    "array": list(work_arr),
                    "highlights": {pi: "sorted"},
                    "pointers": {"pivot": pi},
                    "sorted_indices": sorted(list(sorted_indices))
                },
                "counters": {"swaps": 1}
            }

            recursive_calls += 2
            yield from quick_sort_rec(low, pi - 1)
            yield from quick_sort_rec(pi + 1, high)

        yield from quick_sort_rec(0, n - 1)

        yield {
            "type": "done",
            "message": "Quick Sort finished. Array is fully sorted.",
            "state": {
                "array": list(work_arr),
                "highlights": {idx: "sorted" for idx in range(n)},
                "pointers": {},
                "sorted_indices": list(range(n))
            },
            "counters": {}
        }

    return generator(), sorted(arr)
