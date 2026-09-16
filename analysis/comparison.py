import matplotlib.pyplot as plt


def plot_comparison(results):
    """
    Generates comparison graphs for all algorithms.
    """

    algorithms = [
        result["algorithm"]
        for result in results
    ]

    times = [
        result["execution_time_ms"]
        for result in results
    ]

    comparisons = [
        result["comparisons"]
        for result in results
    ]

    memory = [
        result["memory_kb"]
        for result in results
    ]

    # --------------------------------
    # Execution Time
    # --------------------------------

    plt.figure(figsize=(9, 5))

    plt.bar(algorithms, times)

    plt.title("String Matching - Execution Time")
    plt.xlabel("Algorithm")
    plt.ylabel("Time (ms)")

    plt.xticks(rotation=15)

    plt.tight_layout()
    plt.show()

    # --------------------------------
    # Character Comparisons
    # --------------------------------

    plt.figure(figsize=(9, 5))

    plt.bar(algorithms, comparisons)

    plt.title("String Matching - Character Comparisons")
    plt.xlabel("Algorithm")
    plt.ylabel("Comparisons")

    plt.xticks(rotation=15)

    plt.tight_layout()
    plt.show()

    # --------------------------------
    # Memory
    # --------------------------------

    plt.figure(figsize=(9, 5))

    plt.bar(algorithms, memory)

    plt.title("String Matching - Peak Memory")
    plt.xlabel("Algorithm")
    plt.ylabel("Memory (KB)")

    plt.xticks(rotation=15)

    plt.tight_layout()
    plt.show()