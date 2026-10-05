from typing import Any, Dict, List, Tuple


def run_job_sequencing(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    raw_jobs = list(input_data["jobs"])
    # Sort jobs by profit in descending order
    sorted_jobs = sorted(raw_jobs, key=lambda j: j["profit"], reverse=True)
    n = len(sorted_jobs)

    max_deadline = max(j["deadline"] for j in sorted_jobs) if sorted_jobs else 0
    sort_ops = n * 2
    slot_searches = 0
    greedy_selections = 0

    if mode == "silent":
        slots = [None] * max_deadline
        total_profit = 0
        scheduled_count = 0
        for job in sorted_jobs:
            d = job["deadline"]
            for s in range(min(max_deadline, d) - 1, -1, -1):
                slot_searches += 1
                if slots[s] is None:
                    slots[s] = job
                    total_profit += job["profit"]
                    scheduled_count += 1
                    greedy_selections += 1
                    break
        return {"output": total_profit, "solution": [j["id"] for j in slots if j], "counters": {"sort_ops": sort_ops, "slot_searches": slot_searches, "greedy_selections": greedy_selections}}

    def generator():
        nonlocal slot_searches, greedy_selections
        slots = [None] * max_deadline
        total_profit = 0
        assigned_jobs = []

        yield {
            "type": "init",
            "message": f"Sorted {n} jobs by profit in descending order. Max deadline = {max_deadline}.",
            "state": {
                "jobs": sorted_jobs,
                "slots": [j["id"] if j else "Free" for j in slots],
                "current_job": None,
                "assigned_jobs": [],
                "total_profit": 0
            },
            "counters": {"sort_ops": sort_ops, "slot_searches": 0, "greedy_selections": 0}
        }

        for job in sorted_jobs:
            job_id = job.get("id", "job")
            profit = job["profit"]
            deadline = job["deadline"]
            scheduled = False

            for s in range(min(max_deadline, deadline) - 1, -1, -1):
                slot_searches += 1
                if slots[s] is None:
                    slots[s] = job
                    total_profit += profit
                    scheduled = True
                    greedy_selections += 1
                    assigned_jobs.append(job_id)

                    yield {
                        "type": "schedule",
                        "message": f"Scheduled Job '{job_id}' (profit {profit}) in time slot {s+1} (deadline {deadline}).",
                        "state": {
                            "jobs": sorted_jobs,
                            "slots": [j["id"] if j else "Free" for j in slots],
                            "current_job": job,
                            "assigned_jobs": list(assigned_jobs),
                            "total_profit": total_profit
                        },
                        "counters": {"slot_searches": 1, "greedy_selections": 1}
                    }
                    break

            if not scheduled:
                yield {
                    "type": "skip",
                    "message": f"Could not schedule Job '{job_id}' (profit {profit}) - all slots before deadline {deadline} are filled.",
                    "state": {
                        "jobs": sorted_jobs,
                        "slots": [j["id"] if j else "Free" for j in slots],
                        "current_job": job,
                        "assigned_jobs": list(assigned_jobs),
                        "total_profit": total_profit
                    },
                    "counters": {"slot_searches": 1}
                }

        yield {
            "type": "done",
            "message": f"Job Sequencing complete. Scheduled Jobs: {assigned_jobs}, Max Profit = {total_profit}.",
            "state": {
                "jobs": sorted_jobs,
                "slots": [j["id"] if j else "Free" for j in slots],
                "current_job": None,
                "assigned_jobs": assigned_jobs,
                "total_profit": total_profit
            },
            "counters": {}
        }

    return generator(), 0
