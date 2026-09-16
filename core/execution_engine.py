import time

from algorithms.string.naive_search import naive_search
from algorithms.string.rabin_karp import rabin_karp
from algorithms.string.kmp import kmp_search
from algorithms.string.z_algorithm import z_search


class ExecutionEngine:
    """
    Central engine responsible for executing
    the selected string-matching algorithm.
    """

    def __init__(self):

        self.algorithms = {
            "Naive": naive_search,
            "Rabin-Karp": rabin_karp,
            "KMP": kmp_search,
            "Z Algorithm": z_search
        }

    def execute(self, algorithm_name, text, pattern):

        if algorithm_name not in self.algorithms:
            raise ValueError(
                f"Unknown algorithm: {algorithm_name}"
            )

        algorithm = self.algorithms[algorithm_name]

        start_time = time.perf_counter()

        matches, states, comparisons = algorithm(
            text,
            pattern
        )

        end_time = time.perf_counter()

        execution_time = (
            end_time - start_time
        ) * 1000

        return {
            "algorithm": algorithm_name,
            "text": text,
            "pattern": pattern,
            "matches": matches,
            "states": states,
            "comparisons": comparisons,
            "execution_time_ms": execution_time
        }