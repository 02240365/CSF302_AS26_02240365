"""
Lab 6 - Q1: Rod Cutting

Price table for lengths 1 to 10: 1, 5, 8, 9, 10, 17, 17, 20, 24, 30
(for lengths above 10 the price is p[i] = 3 * i).

  cut_rod_naive(n)       -> plain recursion, tries every first cut      O(2^n)
  cut_rod_memo(n)        -> top-down, remembers each answer              O(n^2)
  cut_rod_bottom_up(n)   -> bottom-up table, no recursion                O(n^2)

Run:  python q1_rod_cutting.py      (n = 25 with the naive version takes a few seconds)
"""

import time

BASE_PRICES = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


def price(i):
    """Price of a piece of length i (p[i] = 3*i for i > 10)."""
    return BASE_PRICES[i - 1] if i <= 10 else 3 * i


calls = 0          # counts recursive calls


# ---------------------------------------------------------------------
# Task 1: naive recursive solution
# ---------------------------------------------------------------------
def cut_rod_naive(n):
    """r(n) = max over first piece i of  price(i) + r(n - i),  r(0) = 0."""
    global calls
    calls += 1
    if n == 0:
        return 0
    return max(price(i) + cut_rod_naive(n - i) for i in range(1, n + 1))


# ---------------------------------------------------------------------
# Task 2: top-down memoized solution
# ---------------------------------------------------------------------
def cut_rod_memo(n, memo=None):
    global calls
    calls += 1
    if memo is None:
        memo = {0: 0}
    if n in memo:                      # already solved: reuse the answer
        return memo[n]
    memo[n] = max(price(i) + cut_rod_memo(n - i, memo) for i in range(1, n + 1))
    return memo[n]


# ---------------------------------------------------------------------
# Task 3: bottom-up tabulated solution (also remembers the first cut)
# ---------------------------------------------------------------------
def cut_rod_bottom_up(n):
    """Returns (best revenue, list of piece lengths, number of loop steps)."""
    r = [0] * (n + 1)                  # r[j] = best revenue for a rod of length j
    first = [0] * (n + 1)              # first[j] = length of the first piece in the best cut
    steps = 0
    for j in range(1, n + 1):          # solve small rods first
        for i in range(1, j + 1):
            steps += 1
            if price(i) + r[j - i] > r[j]:
                r[j] = price(i) + r[j - i]
                first[j] = i
    pieces, j = [], n                  # follow the first cuts to list the pieces
    while j > 0:
        pieces.append(first[j])
        j -= first[j]
    return r[n], sorted(pieces), steps


# ---------------------------------------------------------------------
# Task 4: revenue and pieces for n = 1 to 10
# ---------------------------------------------------------------------
def task4():
    print("Task 4: Maximum revenue and pieces for n = 1 to 10")
    print(f"{'n':>3} | {'revenue':>7} | pieces")
    print("-" * 32)
    for n in range(1, 11):
        best, pieces, _ = cut_rod_bottom_up(n)
        assert best == cut_rod_naive(n) == cut_rod_memo(n)       # all three agree
        print(f"{n:>3} | {best:>7} | {' + '.join(map(str, pieces))}")


# ---------------------------------------------------------------------
# Task 5, 6: recursive calls and time for n = 5, 10, 15, 20, 25
# ---------------------------------------------------------------------
def measure(func, n):
    global calls
    calls = 0
    start = time.perf_counter()
    result = func(n)
    t = time.perf_counter() - start
    return result, calls, t


def task5():
    print("\nTask 5 & 6: Recursive calls and time (ms)")
    print(f"{'n':>3} | {'revenue':>7} | {'naive calls':>12} {'naive ms':>10} | "
          f"{'memo calls':>10} {'memo ms':>8} | {'bottom-up calls':>15} {'loop steps':>10} {'ms':>7}")
    print("-" * 102)
    rows = []
    for n in [5, 10, 15, 20, 25]:
        rn, cn, tn = measure(cut_rod_naive, n)
        rm, cm, tm = measure(cut_rod_memo, n)
        start = time.perf_counter()
        rb, _, steps = cut_rod_bottom_up(n)
        tb = time.perf_counter() - start
        assert rn == rm == rb
        rows.append((n, cn, cm, steps, tn, tm, tb))
        print(f"{n:>3} | {rn:>7} | {cn:>12,} {tn*1000:>10.3f} | {cm:>10,} {tm*1000:>8.3f} | "
              f"{0:>15} {steps:>10} {tb*1000:>7.3f}")
    print("  naive calls = 2^n,  memo calls = 1 + n(n+1)/2,  bottom-up makes no recursive calls")
    return rows


def plot(rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    ns = [r[0] for r in rows]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.semilogy(ns, [r[1] for r in rows], "o-", label="naive (recursive calls)")
    ax1.semilogy(ns, [r[2] for r in rows], "s-", label="memoized (recursive calls)")
    ax1.semilogy(ns, [r[3] for r in rows], "^--", label="bottom-up (loop steps)")
    ax1.set_title("Work done")
    ax1.set_ylabel("count (log scale)")
    ax2.semilogy(ns, [r[4] for r in rows], "o-", label="naive")
    ax2.semilogy(ns, [r[5] for r in rows], "s-", label="memoized")
    ax2.semilogy(ns, [r[6] for r in rows], "^--", label="bottom-up")
    ax2.set_title("Execution time")
    ax2.set_ylabel("time in seconds (log scale)")
    for ax in (ax1, ax2):
        ax.set_xlabel("rod length n")
        ax.set_xticks(ns)
        ax.grid(True, which="both", ls=":", alpha=0.6)
        ax.legend(fontsize=8)
    plt.suptitle("Rod cutting: naive vs memoized vs bottom-up")
    plt.tight_layout()
    plt.savefig("screenshots/q1_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q1_graph.png")


if __name__ == "__main__":
    task4()
    plot(task5())
