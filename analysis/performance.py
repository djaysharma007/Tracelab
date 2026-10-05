import time
import tracemalloc
from typing import Any, Callable, Dict, Tuple
from core.models import PerformanceMetrics


def measure_algorithm_performance(
    alg_func: Callable,
    input_data: Dict[str, Any],
    get_clean_runner: Callable
) -> Tuple[Any, Any, PerformanceMetrics, list]:
    """
    Executes the algorithm in three distinct separate passes:
    Pass 1: Timing pass (warm-up + median perf_counter across runs)
    Pass 2: Peak memory pass via tracemalloc
    Pass 3: Recording pass (step generator for state recorder and counters)
    """

    # --- PASS 3: Recording pass (State & Output) ---
    # We do this first to get output and trace steps, so if it raises validation or size error, we fail early.
    recorder, output, solution = get_clean_runner(alg_func, input_data)
    steps = recorder.get_trace()
    final_counters = steps[-1].counters if steps else {}

    # --- PASS 1: Timing Pass ---
    # 1 Warm-up run
    try:
        _ = alg_func(input_data, mode="silent")
    except Exception:
        pass

    # Measured runs
    num_runs = 5
    run_times = []
    for _ in range(num_runs):
        t0 = time.perf_counter()
        _ = alg_func(input_data, mode="silent")
        t1 = time.perf_counter()
        run_times.append((t1 - t0) * 1000.0)  # ms

    run_times.sort()
    median_time_ms = run_times[num_runs // 2]

    # Batching check for very fast executions (< 0.1 ms)
    if median_time_ms < 0.1:
        batch_size = 50
        t0 = time.perf_counter()
        for _ in range(batch_size):
            _ = alg_func(input_data, mode="silent")
        t1 = time.perf_counter()
        median_time_ms = ((t1 - t0) * 1000.0) / batch_size

    is_reliable = True
    timing_note = None
    if median_time_ms < 0.01:
        is_reliable = False
        timing_note = "Input size is small; measurement is below timer precision."

    # --- PASS 2: Memory Pass ---
    tracemalloc.start()
    try:
        _ = alg_func(input_data, mode="silent")
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    memory_kb = peak / 1024.0

    metrics = PerformanceMetrics(
        execution_time_ms=round(median_time_ms, 4),
        memory_kb=round(memory_kb, 2),
        operations=final_counters,
        is_timing_reliable=is_reliable,
        timing_note=timing_note
    )

    return output, solution, metrics, steps