"""
Lab 5 - Q2: Counting Sort and Radix Sort

  counting_sort(a, k)        -> stable counting sort for integers 0..k     O(n + k)
  radix_sort(a, base)        -> LSD radix sort, counting sort per digit    O(d (n + base))
  merge_sort(a)              -> merge sort (same method as Lab 1)          O(n log n)

Run:  python q2_linear_sorts.py      (takes about 1 minute)
"""

import random
import time


# ---------------------------------------------------------------------
# Task 1: stable counting sort for integers in the range 0..k
# ---------------------------------------------------------------------
def counting_sort(a, k, key=lambda x: x):
    """Returns a new sorted list. key(x) must be an integer in 0..k.
    Stable: items with equal keys keep their original order."""
    count = [0] * (k + 1)
    for x in a:                         # 1. count each key
        count[key(x)] += 1
    total = 0
    for v in range(k + 1):              # 2. prefix sums: count[v] = first position of key v
        count[v], total = total, total + count[v]
    out = [None] * len(a)
    for x in a:                         # 3. place items left to right -> stable
        out[count[key(x)]] = x
        count[key(x)] += 1
    return out


# ---------------------------------------------------------------------
# Task 2: LSD radix sort using counting sort on each digit
# ---------------------------------------------------------------------
def radix_sort(a, base=10):
    """Sort non-negative integers digit by digit, least significant first.
    Each pass is a stable counting sort on one digit (0..base-1)."""
    if not a:
        return []
    out, place, biggest = list(a), 1, max(a)
    while biggest // place > 0:
        out = counting_sort(out, base - 1, key=lambda x: (x // place) % base)
        place *= base
    return out


# ---------------------------------------------------------------------
# Task 3: merge sort (same method as Lab 1)
# ---------------------------------------------------------------------
def merge_sort(a):
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:          # <= keeps merge sort stable
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


# ---------------------------------------------------------------------
# Timing helpers
# ---------------------------------------------------------------------
def timed(func, *args, repeats=3):
    """Best time of a few runs (one run if slow); also checks the result."""
    best = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(*args)
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
        if t > 0.5:
            break
    assert result == sorted(args[0]), f"{func.__name__} gave a wrong result"
    return best


def task4_vary_k():
    print("\nTask 4: n = 100,000, vary k (time in ms)")
    rng = random.Random(4)
    n, rows = 100_000, []
    print(f"{'k':>12} | {'counting sort':>13} | {'merge sort':>10} | winner")
    print("-" * 52)
    for k in [10, 10**3, 10**5, 10**7]:
        data = [rng.randint(0, k) for _ in range(n)]
        tc, tm = timed(counting_sort, data, k), timed(merge_sort, data)
        rows.append((k, tc, tm))
        print(f"{k:>12,} | {tc*1000:>13.1f} | {tm*1000:>10.1f} | {'counting' if tc < tm else 'merge'}")
    return rows


def task5_vary_n():
    print("\nTask 5: k = 10^9, vary n (time in ms)")
    rng = random.Random(5)
    rows = []
    print(f"{'n':>10} | {'radix base 10':>13} | {'radix base 256':>14} | {'merge sort':>10}")
    print("-" * 58)
    for n in [10_000, 50_000, 100_000, 500_000, 1_000_000]:
        data = [rng.randint(0, 10**9) for _ in range(n)]
        t10, t256, tm = timed(radix_sort, data, 10), timed(radix_sort, data, 256), timed(merge_sort, data)
        rows.append((n, t10, t256, tm))
        print(f"{n:>10,} | {t10*1000:>13.1f} | {t256*1000:>14.1f} | {tm*1000:>10.1f}")
    print("  (k = 10^9 has 10 digits in base 10 but only 4 digits in base 256,")
    print("   so base 10 makes 10 passes over the data and base 256 makes 4)")
    return rows


def task7_stability():
    print("\nTask 7: Stability check, sorting (key, original index) pairs by key only")
    keys = [3, 1, 3, 0, 1, 3, 0, 2]
    pairs = [(key, i) for i, key in enumerate(keys)]
    print("  input :", pairs)
    out = counting_sort(pairs, 3, key=lambda p: p[0])
    print("  output:", out)
    print("  equal keys keep their original index order (e.g. key 3: indexes 0, 2, 5)")

    rng = random.Random(7)
    big = [(rng.randint(0, 50), i) for i in range(100_000)]
    out = counting_sort(big, 50, key=lambda p: p[0])
    stable = all(out[i][0] < out[i + 1][0] or (out[i][0] == out[i + 1][0] and out[i][1] < out[i + 1][1])
                 for i in range(len(out) - 1))
    print(f"  100,000 random pairs with keys 0-50: stable = {stable}")


def plot(k_rows, n_rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))
    ks = [r[0] for r in k_rows]
    ax1.loglog(ks, [r[1] for r in k_rows], "o-", label="counting sort  O(n + k)")
    ax1.loglog(ks, [r[2] for r in k_rows], "s-", label="merge sort  O(n log n)")
    ax1.set_title("n = 100,000, varying k")
    ax1.set_xlabel("largest key k (log scale)")
    ax1.set_ylabel("time in seconds (log scale)")
    ns = [r[0] for r in n_rows]
    ax2.loglog(ns, [r[1] for r in n_rows], "o-", label="radix sort, base 10 (10 passes)")
    ax2.loglog(ns, [r[2] for r in n_rows], "^-", label="radix sort, base 256 (4 passes)")
    ax2.loglog(ns, [r[3] for r in n_rows], "s-", label="merge sort  O(n log n)")
    ax2.set_title("k = 10^9, varying n")
    ax2.set_xlabel("n (log scale)")
    for ax in (ax1, ax2):
        ax.grid(True, which="both", ls=":", alpha=0.6)
        ax.legend(fontsize=8)
    plt.suptitle("Linear-time sorts vs merge sort")
    plt.tight_layout()
    plt.savefig("screenshots/q2_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q2_graph.png")


if __name__ == "__main__":
    print("Task 1-3: small example")
    sample = [170, 45, 75, 90, 802, 24, 2, 66]
    print("  input                 :", sample)
    print("  counting sort (k=802) :", counting_sort(sample, 802))
    print("  radix sort, base 10   :", radix_sort(sample, 10))
    print("  radix sort, base 256  :", radix_sort(sample, 256))
    print("  merge sort            :", merge_sort(sample))
    k_rows = task4_vary_k()
    n_rows = task5_vary_n()
    task7_stability()
    plot(k_rows, n_rows)
