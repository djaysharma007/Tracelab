import time
import tracemalloc


def measure_algorithm(algorithm, text, pattern):
    """
    Measures execution time and memory usage
    of an algorithm.
    """

    tracemalloc.start()

    start_time = time.perf_counter()

    matches, states, comparisons = algorithm(
        text,
        pattern
    )

    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    execution_time = (
        end_time - start_time
    ) * 1000

    peak_memory = peak / 1024

    return {
        "matches": matches,
        "states": states,
        "comparisons": comparisons,
        "execution_time_ms": execution_time,
        "memory_kb": peak_memory
    }