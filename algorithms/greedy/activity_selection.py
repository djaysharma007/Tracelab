from typing import Any, Dict, List, Tuple


def run_activity_selection(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    raw_activities = list(input_data["activities"])
    # Sort activities by finish time
    sorted_activities = sorted(raw_activities, key=lambda a: a["finish"])
    n = len(sorted_activities)

    sort_ops = n * max(1, int(round(n**0.5)))
    greedy_selections = 0
    rejections = 0

    if mode == "silent":
        selected = []
        last_finish = -1
        for act in sorted_activities:
            if act["start"] >= last_finish:
                selected.append(act)
                last_finish = act["finish"]
                greedy_selections += 1
            else:
                rejections += 1
        return {"output": selected, "solution": selected, "counters": {"sort_ops": sort_ops, "greedy_selections": greedy_selections, "rejections": rejections}}

    def generator():
        nonlocal greedy_selections, rejections
        selected = []
        rejected = []
        last_finish = -1

        yield {
            "type": "init",
            "message": f"Sorted {n} activities by finish time for Greedy Activity Selection.",
            "state": {
                "activities": sorted_activities,
                "current_activity": None,
                "selected": [],
                "rejected": [],
                "last_finish": -1
            },
            "counters": {"sort_ops": sort_ops, "greedy_selections": 0, "rejections": 0}
        }

        for act in sorted_activities:
            name = act.get("name", "activity")
            s, f = act["start"], act["finish"]

            if s >= last_finish:
                selected.append(act)
                last_finish = f
                greedy_selections += 1
                yield {
                    "type": "select",
                    "message": f"Selected '{name}' [{s}..{f}] - start {s} >= last finish {last_finish - (f - s)}.",
                    "state": {
                        "activities": sorted_activities,
                        "current_activity": act,
                        "selected": list(selected),
                        "rejected": list(rejected),
                        "last_finish": last_finish
                    },
                    "counters": {"greedy_selections": 1}
                }
            else:
                rejected.append(act)
                rejections += 1
                yield {
                    "type": "reject",
                    "message": f"Rejected '{name}' [{s}..{f}] - overlaps with last finish {last_finish}.",
                    "state": {
                        "activities": sorted_activities,
                        "current_activity": act,
                        "selected": list(selected),
                        "rejected": list(rejected),
                        "last_finish": last_finish
                    },
                    "counters": {"rejections": 1}
                }

        yield {
            "type": "done",
            "message": f"Activity Selection complete. Max compatible activities = {len(selected)}.",
            "state": {
                "activities": sorted_activities,
                "current_activity": None,
                "selected": selected,
                "rejected": rejected,
                "last_finish": last_finish
            },
            "counters": {}
        }

    return generator(), []
