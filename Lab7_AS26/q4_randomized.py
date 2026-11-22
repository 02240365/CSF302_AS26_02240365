"""
Lab 7 - Q4: Randomized Algorithms

  quickselect(a, k)        -> k-th smallest with a random pivot      O(n) expected
  miller_rabin(n, rounds)  -> probabilistic primality test           O(rounds * log^3 n)
  trial_division(n)        -> divide by every odd number up to sqrt(n)  O(sqrt n)

Run:  python q4_randomized.py      (about 30 seconds)
"""

import math
import random
import time


# ---------------------------------------------------------------------
# Task 1: randomized quickselect
# ---------------------------------------------------------------------
def quickselect(a, k):
    """Return the k-th smallest element (k = 0 is the smallest).
    Partition around a random pivot, then continue in ONE side only."""
    a = list(a)
    lo, hi = 0, len(a) - 1
    while True:
        if lo == hi:
            return a[lo]
        pivot = a[random.randint(lo, hi)]
        # 3-way partition of a[lo..hi]: < pivot | == pivot | > pivot
        less = [x for x in a[lo:hi + 1] if x < pivot]
        equal = [x for x in a[lo:hi + 1] if x == pivot]
        greater = [x for x in a[lo:hi + 1] if x > pivot]
        a[lo:hi + 1] = less + equal + greater
        if k < lo + len(less):
            hi = lo + len(less) - 1                  # answer is in the "less" part
        elif k < lo + len(less) + len(equal):
            return pivot                             # answer is the pivot itself
        else:
            lo = lo + len(less) + len(equal)         # answer is in the "greater" part


def sort_and_index(a, k):
    return sorted(a)[k]


def best_time(func, *args, repeats=3):
    best = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(*args)
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
    return result, best


def task1():
    print("Task 1: Randomized quickselect vs sorting and indexing (median, best of 3, ms)")
    rng = random.Random(1)
    random.seed(1)
    rows = []
    print(f"{'n':>10} | {'quickselect':>11} | {'sort + index':>12} | {'same answer':>11}")
    print("-" * 54)
    for n in [10**4, 3 * 10**4, 10**5, 3 * 10**5, 10**6]:
        a = [rng.randint(0, 10**9) for _ in range(n)]
        k = n // 2
        q, tq = best_time(quickselect, a, k)
        s, ts = best_time(sort_and_index, a, k)
        rows.append((n, tq, ts))
        print(f"{n:>10,} | {tq*1000:>11.1f} | {ts*1000:>12.1f} | {str(q == s):>11}")
    return rows


# ---------------------------------------------------------------------
# Task 2: Miller-Rabin vs trial division
# ---------------------------------------------------------------------
def miller_rabin(n, rounds=20, rng=random):
    """False = definitely composite, True = probably prime."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:                       # write n - 1 = 2^s * d with d odd
        d //= 2
        s += 1
    for _ in range(rounds):
        a = rng.randint(2, n - 2)           # random base
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue                        # this base says "maybe prime"
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False                    # a is a witness: n is composite
    return True


def miller_rabin_one_round_raw(n, rng):
    """One round with no small-prime shortcut, used for the 561 experiment."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    a = rng.randint(2, n - 2)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def fermat_one_round(n, rng):
    """For comparison: the simpler Fermat test, a^(n-1) = 1 (mod n)."""
    return pow(rng.randint(2, n - 2), n - 1, n) == 1


def trial_division(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for f in range(3, math.isqrt(n) + 1, 2):
        if n % f == 0:
            return False
    return True


def task2():
    print("\nTask 2: Miller-Rabin (20 rounds) vs trial division on 20 random 12-digit numbers")
    rng = random.Random(2)
    nums = [rng.randrange(10**11, 10**12) for _ in range(14)]
    # 6 of the 20 are random 12-digit primes, so both tests also meet some primes
    while len(nums) < 20:
        x = rng.randrange(10**11, 10**12) | 1
        while not trial_division(x):
            x += 2
        nums.append(x)
    rng.shuffle(nums)
    print(f"{'number':>14} | {'Miller-Rabin':>12} | {'trial division':>14} | {'MR ms':>7} | {'TD ms':>8} | agree")
    print("-" * 78)
    tot_mr = tot_td = 0
    all_agree = True
    for n in nums:
        mr, tm = best_time(miller_rabin, n, repeats=1)
        td, tt = best_time(trial_division, n, repeats=1)
        tot_mr, tot_td = tot_mr + tm, tot_td + tt
        all_agree &= mr == td
        word = lambda b: "prime" if b else "composite"
        print(f"{n:>14} | {word(mr):>12} | {word(td):>14} | {tm*1000:>7.3f} | {tt*1000:>8.3f} | {mr == td}")
    print(f"  all 20 agree: {all_agree}.  Total time: Miller-Rabin {tot_mr*1000:.2f} ms, "
          f"trial division {tot_td*1000:.1f} ms")


# ---------------------------------------------------------------------
# Task 3: one round on the Carmichael number 561 = 3 * 11 * 17
# ---------------------------------------------------------------------
def task3():
    print("\nTask 3: One round on the Carmichael number 561 = 3 x 11 x 17, run 1,000 times")
    rng = random.Random(3)
    mr = sum(miller_rabin_one_round_raw(561, rng) for _ in range(1000))
    fe = sum(fermat_one_round(561, rng) for _ in range(1000))
    liars = sum(1 for a in range(2, 560) if miller_rabin_one_round_raw_with_base(561, a))
    print(f"  Miller-Rabin answered 'prime' {mr} times out of 1,000 ({mr / 10:.1f}%)")
    print(f"  (exact chance: {liars} of the 558 possible bases are 'liars' = {liars / 558:.1%})")
    print(f"  For comparison, the Fermat test answered 'prime' {fe} times out of 1,000 ({fe / 10:.1f}%)")
    print(f"  With 10 rounds Miller-Rabin would be fooled with chance about ({liars}/558)^10 = {(liars / 558) ** 10:.1e}")


def miller_rabin_one_round_raw_with_base(n, a):
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def plot(rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    ns = [r[0] for r in rows]
    plt.figure(figsize=(7, 4.2))
    plt.loglog(ns, [r[1] for r in rows], "o-", label="randomized quickselect  O(n) expected")
    plt.loglog(ns, [r[2] for r in rows], "s-", label="sort + index  O(n log n)")
    plt.xlabel("n (log scale)")
    plt.ylabel("time in seconds (log scale)")
    plt.title("Finding the median: quickselect vs sorting")
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("screenshots/q4_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q4_graph.png")


if __name__ == "__main__":
    rows = task1()
    task2()
    task3()
    plot(rows)
