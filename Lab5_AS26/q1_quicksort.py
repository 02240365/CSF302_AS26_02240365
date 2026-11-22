"""
Lab 5 - Q1: Quicksort Variants

Four in-place quicksorts, each counting its comparisons:
  quicksort_lomuto       -> Lomuto partition, pivot = last element
  quicksort_hoare        -> Hoare partition, pivot = first element
  quicksort_randomised   -> Lomuto partition, pivot = random element
  quicksort_three_way    -> 3-way (Dutch national flag) partition, random pivot

All four recurse on the SMALLER part and loop on the larger part, so the
recursion depth is at most log2(n) and sorted inputs never hit the
recursion limit (task 7).

Run:  python q1_quicksort.py      (takes about 2-3 minutes)
"""

import random
import time

comparisons = 0          # global counter, reset before every sort


# ---------------------------------------------------------------------
# Partition schemes (each adds its comparisons to the counter)
# ---------------------------------------------------------------------
def lomuto_partition(a, lo, hi):
    """Pivot = a[hi]. Result: a[lo..p-1] <= pivot, a[p] = pivot, a[p+1..hi] > pivot."""
    global comparisons
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    comparisons += hi - lo                 # one comparison per element scanned
    a[i], a[hi] = a[hi], a[i]
    return i


def hoare_partition(a, lo, hi):
    """Pivot = a[lo]. Two pointers move towards each other and swap
    out-of-place items. Result: a[lo..j] <= pivot <= a[j+1..hi]."""
    global comparisons
    pivot = a[lo]
    i, j, c = lo - 1, hi + 1, 0
    while True:
        i += 1; c += 1
        while a[i] < pivot:
            i += 1; c += 1
        j -= 1; c += 1
        while a[j] > pivot:
            j -= 1; c += 1
        if i >= j:
            comparisons += c
            return j
        a[i], a[j] = a[j], a[i]


def three_way_partition(a, lo, hi):
    """Random pivot. Result: a[lo..lt-1] < pivot, a[lt..gt] == pivot, a[gt+1..hi] > pivot."""
    global comparisons
    r = random.randint(lo, hi)
    a[lo], a[r] = a[r], a[lo]
    pivot = a[lo]
    lt, i, gt, c = lo, lo + 1, hi, 0
    while i <= gt:
        c += 1
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1; i += 1
        else:
            c += 1
            if a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:                           # equal to the pivot: stays in the middle
                i += 1
    comparisons += c
    return lt, gt


# ---------------------------------------------------------------------
# Task 1, 3: Lomuto-based quicksorts (fixed or random pivot)
# Task 7: recurse on the smaller side, loop on the larger side
# ---------------------------------------------------------------------
def _lomuto_sort(a, lo, hi, randomised):
    while lo < hi:
        if randomised:                      # move a random element into the pivot spot
            r = random.randint(lo, hi)
            a[r], a[hi] = a[hi], a[r]
        p = lomuto_partition(a, lo, hi)
        if p - lo < hi - p:
            _lomuto_sort(a, lo, p - 1, randomised)
            lo = p + 1
        else:
            _lomuto_sort(a, p + 1, hi, randomised)
            hi = p - 1


def quicksort_lomuto(a):
    _lomuto_sort(a, 0, len(a) - 1, randomised=False)


def quicksort_randomised(a):
    _lomuto_sort(a, 0, len(a) - 1, randomised=True)


# ---------------------------------------------------------------------
# Task 2: Hoare quicksort
# ---------------------------------------------------------------------
def _hoare_sort(a, lo, hi):
    while lo < hi:
        j = hoare_partition(a, lo, hi)
        if j - lo < hi - j:
            _hoare_sort(a, lo, j)
            lo = j + 1
        else:
            _hoare_sort(a, j + 1, hi)
            hi = j


def quicksort_hoare(a):
    _hoare_sort(a, 0, len(a) - 1)


# ---------------------------------------------------------------------
# Task 4: Three-way (Dutch national flag) quicksort
# ---------------------------------------------------------------------
def _three_way_sort(a, lo, hi):
    while lo < hi:
        lt, gt = three_way_partition(a, lo, hi)
        if lt - lo < hi - gt:
            _three_way_sort(a, lo, lt - 1)
            lo = gt + 1
        else:
            _three_way_sort(a, gt + 1, hi)
            hi = lt - 1


def quicksort_three_way(a):
    _three_way_sort(a, 0, len(a) - 1)


# ---------------------------------------------------------------------
# Task 5, 6: comparisons and time on four input types
# ---------------------------------------------------------------------
VARIANTS = [("Lomuto", quicksort_lomuto), ("Hoare", quicksort_hoare),
            ("Randomised", quicksort_randomised), ("Three-way", quicksort_three_way)]
INPUTS = ["random", "sorted", "reverse", "duplicates"]
SIZES = [1000, 2000, 4000, 8000, 16000]


def make_input(kind, n, rng):
    if kind == "random":
        return [rng.randint(0, 10**6) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    return [rng.randint(0, 9) for _ in range(n)]          # many duplicates: 0 to 9


def measure(sort, data):
    """Return (comparisons, best time in seconds) for sorting a copy of data,
    and check that the result really is sorted."""
    global comparisons
    best_t, first_c = None, None
    for _ in range(3):                      # best of 3 runs, but one run if it is slow
        a = list(data)
        comparisons = 0
        start = time.perf_counter()
        sort(a)
        t = time.perf_counter() - start
        assert a == sorted(data), "sort gave a wrong result"
        first_c = comparisons if first_c is None else first_c
        best_t = t if best_t is None else min(best_t, t)
        if t > 0.2:
            break
    return first_c, best_t


def run_experiment():
    random.seed(5)
    rng = random.Random(5)
    results = {}
    for kind in INPUTS:
        for n in SIZES:
            data = make_input(kind, n, rng)
            for name, sort in VARIANTS:
                results[(kind, n, name)] = measure(sort, data)
    return results


def print_tables(results):
    names = [v[0] for v in VARIANTS]
    for title, k, fmt in [("Comparisons", 0, "{:>12,}"), ("Time (ms)", 1, "{:>12.2f}")]:
        print(f"\nTask 8: {title}")
        print(f"{'input':<11}{'n':>7} |" + "".join(f"{nm:>12}" for nm in names))
        print("-" * 68)
        for kind in INPUTS:
            for n in SIZES:
                vals = [results[(kind, n, nm)][k] * (1000 if k else 1) for nm in names]
                print(f"{kind:<11}{n:>7,} |" + "".join(fmt.format(v) for v in vals))
            print()


def print_growth(results):
    """Comparisons at n = 16,000 divided by n = 8,000:
    about 2.1 means Theta(n log n), about 4 means Theta(n^2)."""
    print("Growth of comparisons when n doubles (8,000 -> 16,000):  ~2.1 = n log n,  ~4 = n^2")
    names = [v[0] for v in VARIANTS]
    print(f"{'input':<11}|" + "".join(f"{nm:>12}" for nm in names))
    print("-" * 60)
    for kind in INPUTS:
        ratios = [results[(kind, 16000, nm)][0] / results[(kind, 8000, nm)][0] for nm in names]
        cells = [f"{r:.2f}" + (" n²" if r > 3.5 else "") for r in ratios]
        print(f"{kind:<11}|" + "".join(f"{c:>12}" for c in cells))


def plot(results):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.9), sharey=True)
    marks = {"Lomuto": "o-", "Hoare": "s-", "Randomised": "^-", "Three-way": "d-"}
    for ax, kind in zip(axes, INPUTS):
        for name, _ in VARIANTS:
            ax.loglog(SIZES, [results[(kind, n, name)][1] for n in SIZES], marks[name], label=name)
        ax.set_title(f"{kind} input")
        ax.set_xlabel("n (log scale)")
        ax.grid(True, which="both", ls=":", alpha=0.6)
    axes[0].set_ylabel("time in seconds (log scale)")
    axes[0].legend(fontsize=8)
    plt.suptitle("Quicksort variants: running time on four input types")
    plt.tight_layout()
    plt.savefig("screenshots/q1_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q1_graph.png")


if __name__ == "__main__":
    print("Q1: Quicksort variants on random, sorted, reverse sorted and duplicate (0-9) inputs")
    print("(every result is checked against sorted(); recursion is on the smaller part only)")
    res = run_experiment()
    print_tables(res)
    print_growth(res)
    plot(res)
