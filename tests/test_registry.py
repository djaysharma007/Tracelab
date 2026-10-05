from core.algorithm_registry import get_all_algorithms, get_algorithm, get_compare_groups


def test_registry_contains_28_algorithms():
    algs = get_all_algorithms()
    assert len(algs) == 28, f"Expected 28 algorithms in registry, found {len(algs)}"


def test_registry_fields():
    for alg in get_all_algorithms():
        assert alg.id is not None
        assert alg.name is not None
        assert alg.category is not None
        assert alg.stage in ["array", "string", "dp", "graph", "greedy"]
        assert "best" in alg.complexity
        assert len(alg.presets) > 0


def test_compare_groups():
    groups = get_compare_groups()
    assert "Sorting" in groups
    assert "Searching" in groups
    assert "String matching" in groups
