"""
CSF302 Assignment 3: Fixing a Slow Quicksort

Both functions sort a list of integers IN PLACE into ascending order.
  quicksort_basic(a)              -> textbook quicksort, last element as pivot
  quicksort_improved(a, cutoff)   -> random pivot + insertion sort for small parts
                                     + recurse on the smaller part only
sorted() / list.sort() are NOT used inside these functions.

Run "python sorts.py" to do the timing experiments (Part C).
"""

import random


# ---------------------------------------------------------------------
# Part A.1  Basic quicksort (Lomuto partition, last element as pivot)
# ---------------------------------------------------------------------
def quicksort_basic(a):
    """Textbook quicksort. Fast on random data, but Theta(n^2) and very
    deep recursion on sorted data or data with many repeated values."""
    _basic(a, 0, len(a) - 1)


def _basic(a, lo, hi):
    if lo < hi:
        p = _lomuto(a, lo, hi)
        _basic(a, lo, p - 1)        # left of the pivot
        _basic(a, p + 1, hi)        # right of the pivot


def _lomuto(a, lo, hi):
    """Lomuto partition: pivot = a[hi].
    Afterwards a[lo..p-1] <= pivot, a[p] = pivot, a[p+1..hi] > pivot."""
    pivot = a[hi]
    i = lo - 1                      # end of the "<= pivot" region
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]   # put the pivot in its final place
    return i + 1


# ---------------------------------------------------------------------
# Part A.2  Improved quicksort
# ---------------------------------------------------------------------
def quicksort_improved(a, cutoff=16):
    """Quicksort with three fixes:
      1. random pivot          -> sorted input is no longer a bad case
      2. insertion sort for parts of size <= cutoff (less overhead)
      3. recurse on the SMALLER part, loop on the larger one
         -> recursion depth is at most log2(n), so no RecursionError
    It also uses a 3-way partition (< pivot, == pivot, > pivot) so that
    many repeated values (e.g. Nu 100 and Nu 500) are handled in one pass."""
    _improved(a, 0, len(a) - 1, cutoff)


def _improved(a, lo, hi, cutoff):
    while hi - lo + 1 > cutoff:
        lt, gt = _partition3(a, lo, hi)
        # now a[lo..lt-1] < pivot, a[lt..gt] == pivot, a[gt+1..hi] > pivot
        if (lt - lo) < (hi - gt):
            _improved(a, lo, lt - 1, cutoff)   # recurse on the smaller left part
            lo = gt + 1                        # loop on the larger right part
        else:
            _improved(a, gt + 1, hi, cutoff)   # recurse on the smaller right part
            hi = lt - 1                        # loop on the larger left part
    _insertion_sort(a, lo, hi)                 # small part left over


def _partition3(a, lo, hi):
    """3-way partition around a RANDOM pivot (Dutch national flag)."""
    r = random.randint(lo, hi)
    a[lo], a[r] = a[r], a[lo]
    pivot = a[lo]
    lt, i, gt = lo, lo + 1, hi
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:                       # equal to pivot: leave it in the middle
            i += 1
    return lt, gt


def _insertion_sort(a, lo, hi):
    """Sort a[lo..hi] by insertion sort (fast for very small parts)."""
    for i in range(lo + 1, hi + 1):
        x = a[i]
        j = i - 1
        while j >= lo and a[j] > x:
            a[j + 1] = a[j]         # shift bigger items one place right
            j -= 1
        a[j + 1] = x


# ---------------------------------------------------------------------
# Part C  Timing experiments
# ---------------------------------------------------------------------
import time

LIMIT = 60.0                        # stop a sort on an input type after 60 s


def make_input(kind, n, seed):
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randint(0, 10**6) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "duplicates":                    # values 0 to 9 only
        return [rng.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


def time_sort(func, data, repeats=3):
    """Best time of a few runs on a fresh copy each time.
    Returns seconds, or the string 'crash' on RecursionError."""
    best = None
    for _ in range(repeats):
        a = list(data)
        start = time.perf_counter()
        try:
            func(a)
        except RecursionError:
            return "crash"
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
        if t > 1.0:                 # slow run: one measurement is enough
            break
    return best


def fmt(t):
    if t is None:
        return "skipped"
    if t == "crash":
        return "CRASH"
    return f"{t * 1000:.3f}"              # milliseconds


def timing_tables():
    sizes = [1000 * 2**k for k in range(7)]     # 1,000 ... 64,000
    kinds = ["random", "sorted", "duplicates"]
    funcs = [("basic", quicksort_basic), ("improved", quicksort_improved),
             ("sorted()", sorted)]
    results = {}
    for kind in kinds:
        print(f"\nInput type: {kind}")
        print(f"{'n':>7} | {'basic (ms)':>10} | {'improved (ms)':>13} | {'sorted() (ms)':>13}")
        print("-" * 54)
        stopped = set()                          # sorts that hit the 60 s limit
        for n in sizes:
            data = make_input(kind, n, seed=n)
            row = {}
            for name, f in funcs:
                if name in stopped:
                    row[name] = None
                    continue
                t = time_sort(f, data)
                row[name] = t
                if t != "crash" and t > LIMIT:
                    stopped.add(name)
            results[(kind, n)] = row
            print(f"{n:>7} | {fmt(row['basic']):>10} | {fmt(row['improved']):>13} | {fmt(row['sorted()']):>13}")
    return sizes, kinds, results


def cutoff_experiment():
    n = 100_000
    data = make_input("random", n, seed=42)
    print(f"\nCutoff experiment (n = {n:,} random, best of 5 runs)")
    times = {}
    for c in [1, 4, 8, 16, 32, 64]:
        best = min(_run(quicksort_improved, data, c) for _ in range(5))
        times[c] = best
        print(f"  cutoff = {c:>2}: {best:.4f} s")
    best_c = min(times, key=times.get)
    print(f"Best cutoff: {best_c}")
    return times, best_c


def _run(func, data, cutoff):
    a = list(data)
    start = time.perf_counter()
    func(a, cutoff)
    return time.perf_counter() - start


class Counted:
    """An int wrapper that counts comparisons and makes every comparison
    a Python-level call (used to separate algorithm cost from language cost)."""
    count = 0
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __lt__(self, o):
        Counted.count += 1
        return self.v < o.v

    def __gt__(self, o):
        Counted.count += 1
        return self.v > o.v

    def __le__(self, o):
        Counted.count += 1
        return self.v <= o.v


def compare_with_sorted(best_c):
    n = 100_000
    data = make_input("random", n, seed=42)
    print(f"\nComparison with sorted() (n = {n:,} random, best of 5 runs)")

    t_ours = min(_run(quicksort_improved, data, best_c) for _ in range(5))
    t_py = min(time_sort(sorted, data, 1) for _ in range(5))
    print(f"  quicksort_improved (cutoff {best_c}): {t_ours:.4f} s")
    print(f"  sorted()                           : {t_py:.4f} s")
    print(f"  sorted() is {t_ours / t_py:.0f}x faster")

    # Same data wrapped in Counted: both now pay for Python-level comparisons.
    wrapped = [Counted(x) for x in data]
    Counted.count = 0
    a = list(wrapped)
    s = time.perf_counter(); quicksort_improved(a, best_c); t1 = time.perf_counter() - s
    c1 = Counted.count
    Counted.count = 0
    s = time.perf_counter(); sorted(wrapped); t2 = time.perf_counter() - s
    c2 = Counted.count
    print("  With Python-level comparisons (Counted objects):")
    print(f"    quicksort_improved: {c1:,} comparisons, {t1:.3f} s")
    print(f"    sorted()          : {c2:,} comparisons, {t2:.3f} s")
    print(f"    comparison ratio {c1 / c2:.2f}x, time ratio {t1 / t2:.2f}x")
    return t_ours, t_py, c1, c2, t1, t2


def plot(sizes, kinds, results, cut_times):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    # fixed colour per sort, so every panel matches the legend
    styles = {"basic": ("o-", "quicksort_basic", "tab:blue"),
              "improved": ("s-", "quicksort_improved", "tab:orange"),
              "sorted()": ("^-", "sorted()", "tab:green")}
    for ax, kind in zip(axes, kinds):
        for name, (st, label, col) in styles.items():
            xs = [n for n in sizes if isinstance(results[(kind, n)][name], float)]
            ys = [results[(kind, n)][name] for n in xs]
            if xs:
                ax.loglog(xs, ys, st, label=label, color=col)
        crashed = [n for n in sizes if results[(kind, n)]["basic"] == "crash"]
        if crashed:
            ax.text(0.04, 0.95, f"basic crashed\n(RecursionError)\nfrom n = {crashed[0]:,}",
                    transform=ax.transAxes, va="top", fontsize=8,
                    bbox=dict(boxstyle="round", fc="white", ec="grey"))
        ax.set_title(f"{kind} input")
        ax.set_xlabel("n (log scale)")
        ax.grid(True, which="both", ls=":", alpha=0.6)
    axes[0].set_ylabel("time in seconds (log scale)")
    handles = [plt.Line2D([], [], color=c, marker=st[0], label=l) for st, l, c in styles.values()]
    axes[2].legend(handles=handles, fontsize=8, loc="lower right")
    plt.tight_layout()
    plt.savefig("timing_graphs.png", dpi=150)

    plt.figure(figsize=(5.5, 3.2))
    cs = list(cut_times)
    plt.plot(cs, [cut_times[c] for c in cs], "o-")
    plt.xscale("log", base=2)
    plt.xticks(cs, [str(c) for c in cs])
    plt.xlabel("cutoff")
    plt.ylabel("time in seconds")
    plt.title("quicksort_improved, n = 100,000 random")
    plt.grid(True, ls=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig("cutoff_graph.png", dpi=150)
    print("\nGraphs saved to timing_graphs.png and cutoff_graph.png")


if __name__ == "__main__":
    sizes, kinds, results = timing_tables()
    cut_times, best_c = cutoff_experiment()
    compare_with_sorted(best_c)
    plot(sizes, kinds, results, cut_times)
