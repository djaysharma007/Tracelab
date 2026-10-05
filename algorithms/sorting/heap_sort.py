from typing import Any, Dict, List, Tuple


def run_heap_sort(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    n = len(arr)
    comparisons = 0
    swaps = 0
    heapify_calls = 0

    if mode == "silent":
        def silent_heapify(a, size, i):
            nonlocal comparisons, swaps, heapify_calls
            heapify_calls += 1
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < size:
                comparisons += 1
                if a[l] > a[largest]:
                    largest = l
            if r < size:
                comparisons += 1
                if a[r] > a[largest]:
                    largest = r
            if largest != i:
                a[i], a[largest] = a[largest], a[i]
                swaps += 1
                silent_heapify(a, size, largest)

        work = list(arr)
        for i in range(n // 2 - 1, -1, -1):
            silent_heapify(work, n, i)
        for i in range(n - 1, 0, -1):
            work[i], work[0] = work[0], work[i]
            swaps += 1
            silent_heapify(work, i, 0)
        return {"output": work, "solution": work, "counters": {"comparisons": comparisons, "swaps": swaps, "heapify_calls": heapify_calls}}

    def generator():
        nonlocal comparisons, swaps, heapify_calls
        work_arr = list(arr)
        sorted_indices = set()

        yield {
            "type": "init",
            "message": f"Starting Heap Sort on array of size {n}.",
            "state": {
                "array": list(work_arr),
                "highlights": {},
                "pointers": {},
                "sorted_indices": []
            },
            "counters": {"comparisons": 0, "swaps": 0, "heapify_calls": 0}
        }

        def heapify(size, i):
            nonlocal comparisons, swaps, heapify_calls
            heapify_calls += 1
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            yield {
                "type": "heapify",
                "message": f"Heapifying subtree rooted at index {i} ({work_arr[i]}).",
                "state": {
                    "array": list(work_arr),
                    "highlights": {i: "pointer", l: "comparing", r: "comparing"} if r < size else ({i: "pointer", l: "comparing"} if l < size else {i: "pointer"}),
                    "pointers": {"root": i},
                    "sorted_indices": sorted(list(sorted_indices))
                },
                "counters": {"heapify_calls": 1}
            }

            if l < size:
                comparisons += 1
                if work_arr[l] > work_arr[largest]:
                    largest = l
            if r < size:
                comparisons += 1
                if work_arr[r] > work_arr[largest]:
                    largest = r

            if largest != i:
                work_arr[i], work_arr[largest] = work_arr[largest], work_arr[i]
                swaps += 1
                yield {
                    "type": "swap",
                    "message": f"Swapped root {work_arr[largest]} with largest child {work_arr[i]} at index {largest}.",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {i: "swapping", largest: "swapping"},
                        "pointers": {"largest": largest},
                        "sorted_indices": sorted(list(sorted_indices))
                    },
                    "counters": {"swaps": 1, "comparisons": 2}
                }
                yield from heapify(size, largest)

        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(n, i)

        yield {
            "type": "heap_built",
            "message": "Max-heap built. Root element is the maximum.",
            "state": {
                "array": list(work_arr),
                "highlights": {0: "pointer"},
                "pointers": {"max": 0},
                "sorted_indices": []
            },
            "counters": {}
        }

        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            work_arr[i], work_arr[0] = work_arr[0], work_arr[i]
            swaps += 1
            sorted_indices.add(i)

            yield {
                "type": "extract_max",
                "message": f"Extracted max element {work_arr[i]} and moved to index {i}.",
                "state": {
                    "array": list(work_arr),
                    "highlights": {i: "sorted"},
                    "pointers": {"max_extracted": i},
                    "sorted_indices": sorted(list(sorted_indices))
                },
                "counters": {"swaps": 1}
            }

            yield from heapify(i, 0)

        sorted_indices.add(0)

        yield {
            "type": "done",
            "message": "Heap Sort finished. Array is fully sorted.",
            "state": {
                "array": list(work_arr),
                "highlights": {idx: "sorted" for idx in range(n)},
                "pointers": {},
                "sorted_indices": list(range(n))
            },
            "counters": {}
        }

    return generator(), sorted(arr)
