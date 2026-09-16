from algorithms.string.naive_search import naive_search
from algorithms.string.rabin_karp import rabin_karp
from algorithms.string.kmp import kmp_search
from algorithms.string.z_algorithm import z_search

from core.execution_engine import ExecutionEngine
from visualization.string_visualizer import StringVisualizer
from analysis.performance import measure_algorithm
from analysis.comparison import plot_comparison


ALGORITHMS = {
    "1": ("Naive", naive_search),
    "2": ("Rabin-Karp", rabin_karp),
    "3": ("KMP", kmp_search),
    "4": ("Z Algorithm", z_search)
}


def print_header():
    print()
    print("=" * 50)
    print("                 TRACELAB")
    print("=" * 50)
    print(" Interactive Advanced Algorithm Laboratory")
    print("=" * 50)
    print()


def print_menu():
    print("STRING MATCHING ALGORITHMS")
    print()
    print("1. Naive String Matching")
    print("2. Rabin-Karp")
    print("3. KMP")
    print("4. Z Algorithm")
    print("5. Compare All Algorithms")
    print("0. Exit")
    print()


def run_single_algorithm():

    print_menu()

    choice = input("Select an option: ").strip()

    if choice == "0":
        return False

    if choice == "5":
        run_comparison()
        return True

    if choice not in ALGORITHMS:

        print()
        print("Invalid choice.")
        return True

    algorithm_name, algorithm = ALGORITHMS[choice]

    print()
    print(f"Selected Algorithm: {algorithm_name}")
    print()

    text = input("Enter text: ")

    pattern = input("Enter pattern: ")

    if not text or not pattern:

        print()
        print("Text and pattern cannot be empty.")
        return True

    print()
    print(f"Running {algorithm_name}...")
    print()

    engine = ExecutionEngine()

    result = engine.execute(
        algorithm_name,
        text,
        pattern
    )

    print("-" * 50)
    print("RESULT")
    print("-" * 50)

    print(
        f"Algorithm        : "
        f"{algorithm_name}"
    )

    print(
        f"Matches          : "
        f"{result['matches']}"
    )

    print(
        f"Comparisons      : "
        f"{result['comparisons']}"
    )

    print(
        f"Execution Time   : "
        f"{result['execution_time_ms']:.4f} ms"
    )

    print(
        f"States Captured  : "
        f"{len(result['states'])}"
    )

    print("-" * 50)

    show = input(
        "Show step-by-step visualization? (y/n): "
    ).strip().lower()

    if show == "y":

        visualizer = StringVisualizer(
            text,
            pattern,
            result["states"],
            algorithm_name
        )

        visualizer.animate()

    return True


def run_comparison():

    print()
    print("=" * 50)
    print("           ALGORITHM COMPARISON")
    print("=" * 50)

    text = input("Enter text: ")

    pattern = input("Enter pattern: ")

    if not text or not pattern:

        print("Text and pattern cannot be empty.")
        return

    results = []

    print()
    print("Running all algorithms...")
    print()

    for algorithm_name, algorithm in ALGORITHMS.values():

        print(
            f"Running {algorithm_name}..."
        )

        performance = measure_algorithm(
            algorithm,
            text,
            pattern
        )

        result = {
            "algorithm": algorithm_name,
            "execution_time_ms":
                performance["execution_time_ms"],
            "comparisons":
                performance["comparisons"],
            "memory_kb":
                performance["memory_kb"],
            "matches":
                performance["matches"]
        }

        results.append(result)

    print()
    print("=" * 70)
    print(
        f"{'Algorithm':<20}"
        f"{'Time (ms)':<15}"
        f"{'Comparisons':<15}"
        f"{'Memory (KB)':<15}"
    )
    print("=" * 70)

    for result in results:

        print(
            f"{result['algorithm']:<20}"
            f"{result['execution_time_ms']:<15.4f}"
            f"{result['comparisons']:<15}"
            f"{result['memory_kb']:<15.2f}"
        )

    print("=" * 70)

    print()
    print("Generating comparison graphs...")

    plot_comparison(results)


def main():

    print_header()

    while True:

        try:

            if not run_single_algorithm():
                print()
                print("Thank you for using TraceLab.")
                break

        except KeyboardInterrupt:

            print()
            print()
            print("Program interrupted.")
            break

        except Exception as error:

            print()
            print(
                f"Error: {error}"
            )


if __name__ == "__main__":
    main()