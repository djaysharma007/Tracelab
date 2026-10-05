import random
import time
import tracemalloc
from typing import Any, Dict, List, Optional
from core.algorithm_registry import get_algorithm
from core.models import ComparePoint, CompareResponse, CompareSeries


def run_benchmark_series(
    algorithm_ids: List[str],
    input_kind: str,
    sizes: List[int],
    repeats: int = 3,
    seed: int = 42,
    alg_runners: Dict[str, Any] = None,
    generator_func: Any = None
) -> CompareResponse:
    """
    Runs fair, seed-reproducible benchmarks across multiple algorithms without recording traces.
    Skipped points (size > max_benchmark_size) are explicitly recorded as skipped.
    """
    if alg_runners is None:
        alg_runners = {}

    series_map: Dict[str, CompareSeries] = {}

    for alg_id in algorithm_ids:
        meta = get_algorithm(alg_id)
        alg_name = meta.name if meta else alg_id
        series_map[alg_id] = CompareSeries(
            algorithm_id=alg_id,
            algorithm_name=alg_name,
            points=[]
        )

    for size in sizes:
        # Generate single seed-consistent input for this size across all algorithms
        rand = random.Random(seed + size)
        test_input = generator_func(input_kind, size, rand) if generator_func else {}

        for alg_id in algorithm_ids:
            meta = get_algorithm(alg_id)
            max_size = meta.max_benchmark_size if meta else 10000

            if size > max_size:
                series_map[alg_id].points.append(
                    ComparePoint(
                        size=size,
                        skipped=True,
                        skip_reason=f"Exceeds max benchmark limit of {max_size}"
                    )
                )
                continue

            alg_func = alg_runners.get(alg_id)
            if not alg_func:
                series_map[alg_id].points.append(
                    ComparePoint(
                        size=size,
                        skipped=True,
                        skip_reason="Algorithm runner not found"
                    )
                )
                continue

            # Silent run without recording steps
            try:
                # 1 Warmup
                _ = alg_func(test_input, mode="silent")

                # Measure Time
                times = []
                for _ in range(repeats):
                    t0 = time.perf_counter()
                    res = alg_func(test_input, mode="silent")
                    t1 = time.perf_counter()
                    times.append((t1 - t0) * 1000.0)

                times.sort()
                med_time = times[len(times) // 2]

                # Measure Memory
                tracemalloc.start()
                res = alg_func(test_input, mode="silent")
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                mem_kb = peak / 1024.0

                # Operations count (silent run returns counters in res if provided)
                ops = res.get("counters", {}) if isinstance(res, dict) else {}

                series_map[alg_id].points.append(
                    ComparePoint(
                        size=size,
                        time_ms=round(med_time, 4),
                        memory_kb=round(mem_kb, 2),
                        operations=ops,
                        skipped=False
                    )
                )
            except Exception as e:
                series_map[alg_id].points.append(
                    ComparePoint(
                        size=size,
                        skipped=True,
                        skip_reason=f"Execution error: {str(e)}"
                    )
                )

    return CompareResponse(
        group=input_kind,
        metrics=["time", "operations", "memory"],
        series=series_map
    )
