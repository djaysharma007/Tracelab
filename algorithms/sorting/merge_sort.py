from typing import Any, Dict, List, Tuple


def run_merge_sort(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    arr = list(input_data["array"])
    n = len(arr)
    comparisons = 0
    merges = 0
    recursive_calls = 0

    if mode == "silent":
        def silent_merge_sort(a):
            nonlocal comparisons, merges, recursive_calls
            if len(a) <= 1:
                return a
            recursive_calls += 2
            mid = len(a) // 2
            left = silent_merge_sort(a[:mid])
            right = silent_merge_sort(a[mid:])

            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                comparisons += 1
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            merges += 1
            return merged

        res = silent_merge_sort(arr)
        return {"output": res, "solution": res, "counters": {"comparisons": comparisons, "merges": merges, "recursive_calls": recursive_calls}}

    def generator():
        nonlocal comparisons, merges, recursive_calls
        work_arr = list(arr)

        yield {
            "type": "init",
            "message": f"Starting Merge Sort on array of size {n}.",
            "state": {
                "array": list(work_arr),
                "highlights": {},
                "pointers": {},
                "subranges": [[0, n - 1]]
            },
            "counters": {"comparisons": 0, "merges": 0, "recursive_calls": 0}
        }

        def merge_sort_rec(l, r):
            nonlocal comparisons, merges, recursive_calls
            if l >= r:
                return

            mid = (l + r) // 2
            recursive_calls += 2

            yield {
                "type": "divide",
                "message": f"Dividing sub-array [{l}..{r}] into [{l}..{mid}] and [{mid+1}..{r}].",
                "state": {
                    "array": list(work_arr),
                    "highlights": {i: "pointer" for i in range(l, r + 1)},
                    "pointers": {"left": l, "mid": mid, "right": r},
                    "subranges": [[l, mid], [mid + 1, r]]
                },
                "counters": {"recursive_calls": 2}
            }

            yield from merge_sort_rec(l, mid)
            yield from merge_sort_rec(mid + 1, r)

            # Merge step
            left_part = work_arr[l:mid + 1]
            right_part = work_arr[mid + 1:r + 1]
            i = j = 0
            k = l

            while i < len(left_part) and j < len(right_part):
                comparisons += 1
                yield {
                    "type": "compare",
                    "message": f"Comparing left element {left_part[i]} at index {l+i} and right element {right_part[j]} at index {mid+1+j}.",
                    "state": {
                        "array": list(work_arr),
                        "highlights": {l + i: "comparing", mid + 1 + j: "comparing"},
                        "pointers": {"left_idx": l + i, "right_idx": mid + 1 + j, "target": k},
                        "subranges": [[l, r]]
                    },
                    "counters": {"comparisons": 1}
                }

                if left_part[i] <= right_part[j]:
                    work_arr[k] = left_part[i]
                    i += 1
                else:
                    work_arr[k] = right_part[j]
                    j += 1
                k += 1

            while i < len(left_part):
                work_arr[k] = left_part[i]
                i += 1
                k += 1

            while j < len(right_part):
                work_arr[k] = right_part[j]
                j += 1
                k += 1

            merges += 1
            yield {
                "type": "merge_complete",
                "message": f"Merged sorted sub-array [{l}..{r}]: {work_arr[l:r+1]}.",
                "state": {
                    "array": list(work_arr),
                    "highlights": {idx: "sorted" for idx in range(l, r + 1)},
                    "pointers": {"merged_left": l, "merged_right": r},
                    "subranges": [[l, r]]
                },
                "counters": {"merges": 1}
            }

        yield from merge_sort_rec(0, n - 1)

        yield {
            "type": "done",
            "message": "Merge Sort finished. Array is fully sorted.",
            "state": {
                "array": list(work_arr),
                "highlights": {idx: "sorted" for idx in range(n)},
                "pointers": {},
                "subranges": []
            },
            "counters": {}
        }

    return generator(), sorted(arr)
