from typing import Any, Dict, List, Optional
from core.models import StepSnapshot


class StateRecorder:
    """
    Captures intermediate step events yielded by algorithms and creates
    standalone snapshots with cumulative counter tracking and step cap enforcement.
    """

    MAX_STEPS = 5000

    def __init__(self):
        self.snapshots: List[StepSnapshot] = []
        self.cumulative_counters: Dict[str, int] = {}

    def record_step(self, step_type: str, message: str, state: Dict[str, Any], delta_counters: Optional[Dict[str, int]] = None):
        if len(self.snapshots) >= self.MAX_STEPS:
            raise ValueError(f"Trace size exceeded the maximum limit of {self.MAX_STEPS} steps. Please provide a smaller input.")

        if delta_counters:
            for key, val in delta_counters.items():
                self.cumulative_counters[key] = self.cumulative_counters.get(key, 0) + val

        snapshot = StepSnapshot(
            index=len(self.snapshots) + 1,
            type=step_type,
            message=message,
            state=state,
            counters=dict(self.cumulative_counters)
        )
        self.snapshots.append(snapshot)

    def get_trace(self) -> List[StepSnapshot]:
        return self.snapshots

    def clear(self):
        self.snapshots.clear()
        self.cumulative_counters.clear()