"""
CSF302 - Lab 1 - Question 1
Empirical Growth Rate Measurement: Linear Search vs Binary Search
"""

import random
import time
import csv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
INPUT_SIZES_365 = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
TRIALS_PER_SIZE_365 = 50  # number of search queries averaged per array size


# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------
def LinearSearch_365(arr, target):
    """Linear Search: scans the list sequentially. Time complexity: O(n)."""
    for index_365, value_365 in enumerate(arr):
        if value_365 == target:
            return index_365
    return -1


def BinarySearch_365(arr, target):
    """Binary Search on a SORTED list. Time complexity: O(log n)."""
    low_365 = 0
    high_365 = len(arr) - 1
    while low_365 <= high_365:
        mid_365 = (low_365 + high_365) // 2
        if arr[mid_365] == target:
            return mid_365
        elif arr[mid_365] < target:
            low_365 = mid_365 + 1
        else:
            high_365 = mid_365 - 1
    return -1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def GenerateRandomArray_365(size_365):
    """Generates a list of `size_365` unique random integers."""
    return random.sample(range(size_365 * 10), size_365)


def GenerateTargets_365(arr_365, count_365):
    """Generates a mix of targets that ARE and ARE NOT present in the array,
    so the average time reflects both best/average and worst-case searches."""
    targets_365 = []
    for _ in range(count_365 // 2):
        targets_365.append(random.choice(arr_365))            # present value
    for _ in range(count_365 - count_365 // 2):
        targets_365.append(random.randint(-10_000, -1))       # guaranteed absent
    random.shuffle(targets_365)
    return targets_365


def MeasureAlgorithm_365(search_func_365, arr_365, targets_365):
    """Runs search_func_365 against every target and returns the AVERAGE
    execution time in seconds."""
    start_365 = time.perf_counter()
    for target_365 in targets_365:
        search_func_365(arr_365, target_365)
    end_365 = time.perf_counter()
    total_time_365 = end_365 - start_365
    return total_time_365 / len(targets_365)


# ---------------------------------------------------------------------------
# Benchmark driver
# ---------------------------------------------------------------------------
def RunBenchmark_365():
    results_365 = []
    print(f"{'N':>10} | {'Linear Search (s)':>20} | {'Binary Search (s)':>20}")
    print("-" * 58)

    for size_365 in INPUT_SIZES_365:
        base_array_365 = GenerateRandomArray_365(size_365)
        sorted_array_365 = sorted(base_array_365)
        targets_365 = GenerateTargets_365(base_array_365, TRIALS_PER_SIZE_365)

        linear_avg_365 = MeasureAlgorithm_365(LinearSearch_365, base_array_365, targets_365)
        binary_avg_365 = MeasureAlgorithm_365(BinarySearch_365, sorted_array_365, targets_365)

        results_365.append((size_365, linear_avg_365, binary_avg_365))
        print(f"{size_365:>10} | {linear_avg_365:>20.8f} | {binary_avg_365:>20.8f}")

    return results_365


def SaveResultsToCSV_365(results_365, filename_365="Lab1_Q1_Results.csv"):
    with open(filename_365, "w", newline="") as file_365:
        writer_365 = csv.writer(file_365)
        writer_365.writerow(["N", "Linear_Search_Avg_Time_s", "Binary_Search_Avg_Time_s"])
        writer_365.writerows(results_365)
    print(f"\nResults saved to {filename_365}")


def PlotResults_365(results_365, filename_365="Lab1_Q1_Plot.png"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping plot generation.")
        return

    sizes_365 = [row_365[0] for row_365 in results_365]
    linear_365 = [row_365[1] for row_365 in results_365]
    binary_365 = [row_365[2] for row_365 in results_365]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes_365, linear_365, marker="o", label="Linear Search - O(n)")
    plt.plot(sizes_365, binary_365, marker="o", label="Binary Search - O(log n)")
    plt.xlabel("Input Size (N)")
    plt.ylabel("Average Execution Time (seconds)")
    plt.title("Linear Search vs Binary Search - Empirical Growth Rate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename_365)
    print(f"Plot saved to {filename_365}")


if __name__ == "__main__":
    results_365 = RunBenchmark_365()
    SaveResultsToCSV_365(results_365)
    PlotResults_365(results_365)
