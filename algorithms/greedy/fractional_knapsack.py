from typing import Any, Dict, List, Tuple


def run_fractional_knapsack(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    raw_items = list(input_data["items"])
    capacity = float(input_data["capacity"])

    # Compute value/weight ratios
    items = []
    for item in raw_items:
        w = float(item["weight"])
        v = float(item["value"])
        ratio = v / w if w > 0 else 0
        items.append({
            "name": item.get("name", "Item"),
            "weight": w,
            "value": v,
            "ratio": round(ratio, 2)
        })

    sorted_items = sorted(items, key=lambda x: x["ratio"], reverse=True)
    n = len(sorted_items)

    ratio_calcs = n
    sort_ops = n * 2
    greedy_selections = 0

    if mode == "silent":
        total_value = 0.0
        rem_cap = capacity
        takes = []
        for item in sorted_items:
            if rem_cap <= 0:
                break
            if item["weight"] <= rem_cap:
                takes.append({"item": item, "fraction": 1.0, "value": item["value"]})
                total_value += item["value"]
                rem_cap -= item["weight"]
            else:
                fraction = rem_cap / item["weight"]
                val = item["value"] * fraction
                takes.append({"item": item, "fraction": round(fraction, 2), "value": round(val, 2)})
                total_value += val
                rem_cap = 0
            greedy_selections += 1
        return {"output": round(total_value, 2), "solution": takes, "counters": {"ratio_calcs": ratio_calcs, "sort_ops": sort_ops, "greedy_selections": greedy_selections}}

    def generator():
        nonlocal greedy_selections
        total_value = 0.0
        rem_cap = capacity
        takes = []

        yield {
            "type": "init",
            "message": f"Sorted {n} items by value/weight ratio for capacity {capacity}.",
            "state": {
                "items": sorted_items,
                "capacity": capacity,
                "remaining_capacity": rem_cap,
                "current_item": None,
                "taken_items": [],
                "total_value": 0.0
            },
            "counters": {"ratio_calcs": ratio_calcs, "sort_ops": sort_ops, "greedy_selections": 0}
        }

        for item in sorted_items:
            if rem_cap <= 0:
                break
            greedy_selections += 1
            if item["weight"] <= rem_cap:
                takes.append({"name": item["name"], "fraction": 1.0, "weight": item["weight"], "value": item["value"]})
                total_value += item["value"]
                rem_cap -= item["weight"]
                msg = f"Took 100% of '{item['name']}' (weight {item['weight']}, value {item['value']})."
            else:
                fraction = rem_cap / item["weight"]
                val = item["value"] * fraction
                takes.append({"name": item["name"], "fraction": round(fraction, 2), "weight": round(rem_cap, 2), "value": round(val, 2)})
                total_value += val
                rem_cap = 0
                msg = f"Took {round(fraction*100, 1)}% fraction of '{item['name']}' (value {round(val, 2)})."

            yield {
                "type": "take_item",
                "message": msg,
                "state": {
                    "items": sorted_items,
                    "capacity": capacity,
                    "remaining_capacity": round(rem_cap, 2),
                    "current_item": item,
                    "taken_items": list(takes),
                    "total_value": round(total_value, 2)
                },
                "counters": {"greedy_selections": 1}
            }

        yield {
            "type": "done",
            "message": f"Fractional Knapsack complete. Max Total Value = {round(total_value, 2)}.",
            "state": {
                "items": sorted_items,
                "capacity": capacity,
                "remaining_capacity": round(rem_cap, 2),
                "current_item": None,
                "taken_items": takes,
                "total_value": round(total_value, 2)
            },
            "counters": {}
        }

    return generator(), 0
