"""
CSF302 - Lab 1 - Question 3
Empirical Growth Rate Measurement: Prime Number Generation
    1. Naive Prime Checking using Trial Division
    2. Optimized Trial Division (checking up to sqrt(n))
    3. Sieve of Eratosthenes
"""

import time
import csv
import math

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
INPUT_SIZES_365 = [10_000, 50_000, 100_000, 500_000, 1_000_000]

# The naive method is O(N^2) overall (it checks EVERY divisor for EVERY
# number up to N). For N = 500,000 / 1,000,000 this becomes impractically
# slow (potentially hours). This cap keeps the benchmark runnable; raise it
# only if you are willing to let it run for a very long time.
NAIVE_MAX_N_365 = 100_000


# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------
def IsPrimeNaive_365(n_365):
    """Naive primality test: divides n by EVERY integer from 2 to n-1.
    Time complexity: O(n)."""
    if n_365 < 2:
        return False
    for divisor_365 in range(2, n_365):
        if n_365 % divisor_365 == 0:
            return False
    return True


def GeneratePrimesNaive_365(limit_365):
    """Generates all primes up to `limit_365` using naive trial division.
    Overall time complexity: O(n^2)."""
    primes_365 = []
    for number_365 in range(2, limit_365 + 1):
        if IsPrimeNaive_365(number_365):
            primes_365.append(number_365)
    return primes_365


def IsPrimeOptimized_365(n_365):
    """Optimized primality test: only checks divisors up to sqrt(n).
    Time complexity: O(sqrt(n))."""
    if n_365 < 2:
        return False
    if n_365 in (2, 3):
        return True
    if n_365 % 2 == 0:
        return False
    limit_365 = int(math.isqrt(n_365))
    for divisor_365 in range(3, limit_365 + 1, 2):
        if n_365 % divisor_365 == 0:
            return False
    return True


def GeneratePrimesOptimized_365(limit_365):
    """Generates all primes up to `limit_365` using optimized trial division.
    Overall time complexity: O(n * sqrt(n))."""
    primes_365 = []
    for number_365 in range(2, limit_365 + 1):
        if IsPrimeOptimized_365(number_365):
            primes_365.append(number_365)
    return primes_365


def GeneratePrimesSieve_365(limit_365):
    """Generates all primes up to `limit_365` using the Sieve of Eratosthenes.
    Time complexity: O(n log log n)."""
    if limit_365 < 2:
        return []

    is_prime_365 = [True] * (limit_365 + 1)
    is_prime_365[0] = is_prime_365[1] = False

    for number_365 in range(2, int(math.isqrt(limit_365)) + 1):
        if is_prime_365[number_365]:
            for multiple_365 in range(number_365 * number_365, limit_365 + 1, number_365):
                is_prime_365[multiple_365] = False

    return [i_365 for i_365, flag_365 in enumerate(is_prime_365) if flag_365]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def TimeFunction_365(func_365, *args_365):
    """Times a single call to func_365 and returns (elapsed_seconds, result)."""
    start_365 = time.perf_counter()
    result_365 = func_365(*args_365)
    end_365 = time.perf_counter()
    return end_365 - start_365, result_365


# ---------------------------------------------------------------------------
# Benchmark driver
# ---------------------------------------------------------------------------
def RunBenchmark_365():
    results_365 = []
    print(f"{'N':>10} | {'Naive (s)':>14} | {'Optimized (s)':>14} | {'Sieve (s)':>14}")
    print("-" * 62)

    for size_365 in INPUT_SIZES_365:
        if size_365 <= NAIVE_MAX_N_365:
            naive_time_365, _ = TimeFunction_365(GeneratePrimesNaive_365, size_365)
            naive_display_365 = f"{naive_time_365:.6f}"
        else:
            naive_time_365 = None
            naive_display_365 = "SKIPPED"
            print(f"(Naive trial division skipped for N={size_365}: "
                  f"O(n^2) complexity makes it impractically slow.)")

        opt_time_365, _ = TimeFunction_365(GeneratePrimesOptimized_365, size_365)
        sieve_time_365, _ = TimeFunction_365(GeneratePrimesSieve_365, size_365)

        results_365.append((size_365, naive_time_365, opt_time_365, sieve_time_365))
        print(f"{size_365:>10} | {naive_display_365:>14} | {opt_time_365:>14.6f} | {sieve_time_365:>14.6f}")

    return results_365


def SaveResultsToCSV_365(results_365, filename_365="Lab1_Q3_Results.csv"):
    with open(filename_365, "w", newline="") as file_365:
        writer_365 = csv.writer(file_365)
        writer_365.writerow(["N", "Naive_Time_s", "Optimized_Time_s", "Sieve_Time_s"])
        for row_365 in results_365:
            n_365, naive_365, opt_365, sieve_365 = row_365
            writer_365.writerow([n_365, naive_365 if naive_365 is not None else "SKIPPED", opt_365, sieve_365])
    print(f"\nResults saved to {filename_365}")


def PlotResults_365(results_365, filename_365="Lab1_Q3_Plot.png"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping plot generation.")
        return

    sizes_365 = [row_365[0] for row_365 in results_365]
    naive_sizes_365 = [row_365[0] for row_365 in results_365 if row_365[1] is not None]
    naive_times_365 = [row_365[1] for row_365 in results_365 if row_365[1] is not None]
    opt_365 = [row_365[2] for row_365 in results_365]
    sieve_365 = [row_365[3] for row_365 in results_365]

    plt.figure(figsize=(8, 5))
    if naive_times_365:
        plt.plot(naive_sizes_365, naive_times_365, marker="o", label="Naive Trial Division - O(n^2)")
    plt.plot(sizes_365, opt_365, marker="o", label="Optimized Trial Division - O(n*sqrt n)")
    plt.plot(sizes_365, sieve_365, marker="o", label="Sieve of Eratosthenes - O(n log log n)")
    plt.xlabel("N (upper limit)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Prime Generation Methods - Empirical Growth Rate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename_365)
    print(f"Plot saved to {filename_365}")


if __name__ == "__main__":
    results_365 = RunBenchmark_365()
    SaveResultsToCSV_365(results_365)
    PlotResults_365(results_365)
