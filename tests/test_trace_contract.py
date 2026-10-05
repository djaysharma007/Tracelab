import pytest
from core.algorithm_registry import get_all_algorithms
from core.execution_engine import ExecutionEngine

engine = ExecutionEngine()


def test_trace_contract_all_algorithms_presets():
    all_algs = get_all_algorithms()
    for meta in all_algs:
        for preset in meta.presets:
            res = engine.execute(meta.id, preset.input)
            steps = res.steps

            assert len(steps) > 0, f"Algorithm {meta.id} preset '{preset.name}' produced no steps."

            # Check 1-based indexing
            for i, step in enumerate(steps):
                assert step.index == i + 1, f"Step index mismatch in {meta.id}: {step.index} vs {i+1}"
                assert step.type is not None
                assert isinstance(step.message, str)
                assert isinstance(step.state, dict)

            # Check cumulative counters never decrease
            prev_counters = {}
            for step in steps:
                for cnt_key, cnt_val in step.counters.items():
                    if cnt_key in prev_counters:
                        assert cnt_val >= prev_counters[cnt_key], (
                            f"Counter '{cnt_key}' decreased from {prev_counters[cnt_key]} to {cnt_val} "
                            f"in algorithm '{meta.id}' at step {step.index}"
                        )
                    prev_counters[cnt_key] = cnt_val

            # Check final step is marked done
            assert steps[-1].type == "done", f"Final step of {meta.id} preset '{preset.name}' is not 'done'."
