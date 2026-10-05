from typing import Any, Dict, Tuple
from core.algorithm_registry import get_algorithm
from core.models import RunResult
from core.state_recorder import StateRecorder
from analysis.performance import measure_algorithm_performance
from input.input_handler import validate_algorithm_input

from algorithms.sorting.bubble_sort import run_bubble_sort
from algorithms.sorting.selection_sort import run_selection_sort
from algorithms.sorting.insertion_sort import run_insertion_sort
from algorithms.sorting.merge_sort import run_merge_sort
from algorithms.sorting.quick_sort import run_quick_sort
from algorithms.sorting.heap_sort import run_heap_sort

from algorithms.searching.linear_search import run_linear_search
from algorithms.searching.binary_search import run_binary_search

from algorithms.string.naive_search import run_naive_search
from algorithms.string.rabin_karp import run_rabin_karp
from algorithms.string.kmp_search import run_kmp_search
from algorithms.string.z_search import run_z_search

from algorithms.dynamic_programming.knapsack_01 import run_knapsack_01
from algorithms.dynamic_programming.lcs import run_lcs
from algorithms.dynamic_programming.lis import run_lis
from algorithms.dynamic_programming.mcm import run_mcm
from algorithms.dynamic_programming.edit_distance import run_edit_distance

from algorithms.graph.bfs import run_bfs
from algorithms.graph.dfs import run_dfs
from algorithms.graph.dijkstra import run_dijkstra
from algorithms.graph.bellman_ford import run_bellman_ford
from algorithms.graph.floyd_warshall import run_floyd_warshall
from algorithms.graph.prim import run_prim
from algorithms.graph.kruskal import run_kruskal

from algorithms.greedy.activity_selection import run_activity_selection
from algorithms.greedy.fractional_knapsack import run_fractional_knapsack
from algorithms.greedy.huffman_coding import run_huffman_coding
from algorithms.greedy.job_sequencing import run_job_sequencing


ALGORITHM_MAP = {
    "bubble_sort": run_bubble_sort,
    "selection_sort": run_selection_sort,
    "insertion_sort": run_insertion_sort,
    "merge_sort": run_merge_sort,
    "quick_sort": run_quick_sort,
    "heap_sort": run_heap_sort,
    "linear_search": run_linear_search,
    "binary_search": run_binary_search,
    "naive_search": run_naive_search,
    "rabin_karp": run_rabin_karp,
    "kmp_search": run_kmp_search,
    "z_search": run_z_search,
    "knapsack_01": run_knapsack_01,
    "lcs": run_lcs,
    "lis": run_lis,
    "mcm": run_mcm,
    "edit_distance": run_edit_distance,
    "bfs": run_bfs,
    "dfs": run_dfs,
    "dijkstra": run_dijkstra,
    "bellman_ford": run_bellman_ford,
    "floyd_warshall": run_floyd_warshall,
    "prim": run_prim,
    "kruskal": run_kruskal,
    "activity_selection": run_activity_selection,
    "fractional_knapsack": run_fractional_knapsack,
    "huffman_coding": run_huffman_coding,
    "job_sequencing": run_job_sequencing,
}


def _run_generator_and_record(alg_func: Any, input_data: Dict[str, Any]) -> Tuple[StateRecorder, Any, Any]:
    recorder = StateRecorder()
    gen, solution = alg_func(input_data, mode="record")
    last_output = solution
    for event in gen:
        recorder.record_step(
            step_type=event.get("type", "step"),
            message=event.get("message", ""),
            state=event.get("state", {}),
            delta_counters=event.get("counters")
        )
        if "output" in event.get("state", {}):
            last_output = event["state"]["output"]
    return recorder, last_output, solution


class ExecutionEngine:
    """
    Central execution engine coordinating validation, state recording,
    and 3-pass separate performance measurement for all 28 algorithms.
    """

    def __init__(self):
        self.algorithm_map = ALGORITHM_MAP

    def execute(self, algorithm_id: str, input_data: Dict[str, Any]) -> RunResult:
        if algorithm_id not in self.algorithm_map:
            raise ValueError(f"Algorithm '{algorithm_id}' is not registered.")

        meta = get_algorithm(algorithm_id)

        # Input Validation
        validated_input = validate_algorithm_input(algorithm_id, input_data)

        # Enforce max visual size cap
        if meta and meta.max_visual_size:
            arr_len = len(validated_input.get("array", [])) or len(validated_input.get("text", ""))
            if arr_len > meta.max_visual_size:
                raise ValueError(f"Input size ({arr_len}) exceeds maximum visualizer limit of {meta.max_visual_size} items.")

        alg_func = self.algorithm_map[algorithm_id]

        # Perform 3-pass measurement
        output, solution, metrics, steps = measure_algorithm_performance(
            alg_func=alg_func,
            input_data=validated_input,
            get_clean_runner=_run_generator_and_record
        )

        return RunResult(
            algorithm_id=algorithm_id,
            algorithm_name=meta.name if meta else algorithm_id,
            input=validated_input,
            output=output,
            solution=solution,
            steps=steps,
            total_steps=len(steps),
            metrics=metrics
        )