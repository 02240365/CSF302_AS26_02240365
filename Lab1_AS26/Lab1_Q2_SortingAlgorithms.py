"""
CSF302 - Lab 1 - Question 2
Empirical Growth Rate Measurement: Bubble Sort vs Merge Sort
"""

import random
import time
import csv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
INPUT_SIZES_365 = [100, 500, 1_000, 2_000, 4_000, 8_000]
TRIALS_PER_SIZE_365 = 5  # number of repeated trials averaged per array size


# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------
def BubbleSort_365(arr_365):
    """Bubble Sort: repeatedly swaps adjacent out-of-order elements.
    Time complexity: O(n^2)."""
    a_365 = arr_365.copy()
    n_365 = len(a_365)
    for i_365 in range(n_365 - 1):
        swapped_365 = False
        for j_365 in range(n_365 - 1 - i_365):
            if a_365[j_365] > a_365[j_365 + 1]:
                a_365[j_365], a_365[j_365 + 1] = a_365[j_365 + 1], a_365[j_365]
                swapped_365 = True
        if not swapped_365:
            break
    return a_365


def MergeSort_365(arr_365):
    """Merge Sort: divide-and-conquer sorting. Time complexity: O(n log n)."""
    if len(arr_365) <= 1:
        return arr_365.copy()

    mid_365 = len(arr_365) // 2
    left_365 = MergeSort_365(arr_365[:mid_365])
    right_365 = MergeSort_365(arr_365[mid_365:])
    return Merge_365(left_365, right_365)


def Merge_365(left_365, right_365):
    """Merges two already-sorted lists into a single sorted list."""
    merged_365 = []
    i_365 = j_365 = 0
    while i_365 < len(left_365) and j_365 < len(right_365):
        if left_365[i_365] <= right_365[j_365]:
            merged_365.append(left_365[i_365])
            i_365 += 1
        else:
            merged_365.append(right_365[j_365])
            j_365 += 1
    merged_365.extend(left_365[i_365:])
    merged_365.extend(right_365[j_365:])
    return merged_365


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def GenerateRandomArray_365(size_365):
    """Generates a list of `size_365` random integers (duplicates allowed)."""
    return [random.randint(0, size_365 * 10) for _ in range(size_365)]


def MeasureSort_365(sort_func_365, size_365):
    """Runs sort_func_365 over TRIALS_PER_SIZE_365 fresh random arrays and
    returns the AVERAGE execution time in seconds."""
    total_time_365 = 0.0
    for _ in range(TRIALS_PER_SIZE_365):
        test_array_365 = GenerateRandomArray_365(size_365)
        start_365 = time.perf_counter()
        sort_func_365(test_array_365)
        end_365 = time.perf_counter()
        total_time_365 += (end_365 - start_365)
    return total_time_365 / TRIALS_PER_SIZE_365


# ---------------------------------------------------------------------------
# Benchmark driver
# ---------------------------------------------------------------------------
def RunBenchmark_365():
    results_365 = []
    print(f"{'N':>8} | {'Bubble Sort (s)':>18} | {'Merge Sort (s)':>18}")
    print("-" * 50)

    for size_365 in INPUT_SIZES_365:
        bubble_avg_365 = MeasureSort_365(BubbleSort_365, size_365)
        merge_avg_365 = MeasureSort_365(MergeSort_365, size_365)
        results_365.append((size_365, bubble_avg_365, merge_avg_365))
        print(f"{size_365:>8} | {bubble_avg_365:>18.6f} | {merge_avg_365:>18.6f}")

    return results_365


def SaveResultsToCSV_365(results_365, filename_365="Lab1_Q2_Results.csv"):
    with open(filename_365, "w", newline="") as file_365:
        writer_365 = csv.writer(file_365)
        writer_365.writerow(["N", "Bubble_Sort_Avg_Time_s", "Merge_Sort_Avg_Time_s"])
        writer_365.writerows(results_365)
    print(f"\nResults saved to {filename_365}")


def PlotResults_365(results_365, filename_365="Lab1_Q2_Plot.png"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping plot generation.")
        return

    sizes_365 = [row_365[0] for row_365 in results_365]
    bubble_365 = [row_365[1] for row_365 in results_365]
    merge_365 = [row_365[2] for row_365 in results_365]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes_365, bubble_365, marker="o", label="Bubble Sort - O(n^2)")
    plt.plot(sizes_365, merge_365, marker="o", label="Merge Sort - O(n log n)")
    plt.xlabel("Input Size (N)")
    plt.ylabel("Average Execution Time (seconds)")
    plt.title("Bubble Sort vs Merge Sort - Empirical Growth Rate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename_365)
    print(f"Plot saved to {filename_365}")


if __name__ == "__main__":
    results_365 = RunBenchmark_365()
    SaveResultsToCSV_365(results_365)
    PlotResults_365(results_365)
