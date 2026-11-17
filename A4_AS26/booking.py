"""
CSF302 Assignment 4: Booking the Hall

Each request is (start, finish, fee). Two requests fit together if one
finishes no later than the other starts (ending at 12 and starting at 12 is fine).
Every function returns (total_fee, chosen): chosen = sorted list of request indices.

  greedy_earliest_finish(requests)  -> the manager's rule
  greedy_highest_fee(requests)      -> another greedy rule
  best_schedule(requests)           -> dynamic programming (always optimal)
  brute_force(requests)             -> tries every subset (checking only, n <= 15)

Run "python booking.py" to do the analysis for Part C.
"""

from bisect import bisect_right
from itertools import combinations


def fits(a, b):
    """True if requests a and b can both use the hall."""
    return a[1] <= b[0] or b[1] <= a[0]


# ---------------------------------------------------------------------
# Part A.1  Greedy: earliest finish first        O(n log n)
# ---------------------------------------------------------------------
def greedy_earliest_finish(requests):
    order = sorted(range(len(requests)), key=lambda i: requests[i][1])  # by finish
    chosen, total = [], 0
    last_finish = float("-inf")
    for i in order:
        start, finish, fee = requests[i]
        if start >= last_finish:            # fits after the last accepted event
            chosen.append(i)
            total += fee
            last_finish = finish
    return total, sorted(chosen)


# ---------------------------------------------------------------------
# Part A.2  Greedy: highest fee first            O(n^2)
# ---------------------------------------------------------------------
def greedy_highest_fee(requests):
    order = sorted(range(len(requests)), key=lambda i: -requests[i][2])  # by fee, high first
    chosen, total = [], 0
    for i in order:
        # accept only if it fits with every request accepted so far
        if all(fits(requests[i], requests[k]) for k in chosen):
            chosen.append(i)
            total += requests[i][2]
    return total, sorted(chosen)


# ---------------------------------------------------------------------
# Part A.3  Dynamic programming                  O(n log n)
# ---------------------------------------------------------------------
def best_schedule(requests):
    """Weighted interval scheduling.
    Sort by finish time. p(j) = number of requests (in sorted order) that
    finish no later than request j starts. Then
        OPT(j) = max( OPT(j-1),  fee_j + OPT(p(j)) ),   OPT(0) = 0
    i.e. either skip request j, or take it and add the best schedule of the
    requests that end before it starts."""
    n = len(requests)
    order = sorted(range(n), key=lambda i: requests[i][1])   # indices by finish
    finishes = [requests[i][1] for i in order]

    # p[j] for j = 1..n (1-based, so OPT[0] = 0 means "no requests")
    p = [0] * (n + 1)
    for j in range(1, n + 1):
        start = requests[order[j - 1]][0]
        p[j] = bisect_right(finishes, start, 0, j - 1)   # binary search

    opt = [0] * (n + 1)
    for j in range(1, n + 1):
        fee = requests[order[j - 1]][2]
        opt[j] = max(opt[j - 1], fee + opt[p[j]])

    # Reconstruct: walk back from j = n, taking j whenever that gave OPT(j)
    chosen, j = [], n
    while j > 0:
        fee = requests[order[j - 1]][2]
        if fee + opt[p[j]] >= opt[j - 1]:     # taking j is (one) best choice
            chosen.append(order[j - 1])
            j = p[j]
        else:
            j -= 1
    return opt[n], sorted(chosen)


# ---------------------------------------------------------------------
# Part A.4  Brute force (for checking only)      O(2^n * n^2)
# ---------------------------------------------------------------------
def brute_force(requests):
    n = len(requests)
    if n > 15:
        raise ValueError("brute_force is only for n <= 15")
    best_total, best_set = 0, []
    for mask in range(1 << n):                       # every subset
        subset = [i for i in range(n) if mask >> i & 1]
        if all(fits(requests[a], requests[b]) for a, b in combinations(subset, 2)):
            total = sum(requests[i][2] for i in subset)
            if total > best_total:
                best_total, best_set = total, subset
    return best_total, best_set


# ---------------------------------------------------------------------
# Part C  Analysis
# ---------------------------------------------------------------------
import random

EXAMPLE = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]

# Counterexamples (Part C.1)
CE_EARLIEST = [(9, 11, 1000), (10, 17, 8000)]                 # cheap early event blocks a big one
CE_HIGHEST = [(9, 17, 8000), (9, 13, 5000), (13, 17, 5000)]   # one big event blocks two medium ones


def random_requests(n, rng):
    """n random requests in one day: start 8:00-19:00, length 1-5 hours,
    fee Nu 1,000-10,000 (in steps of 500)."""
    reqs = []
    for _ in range(n):
        start = rng.randint(8, 19)
        reqs.append((start, start + rng.randint(1, 5), 500 * rng.randint(2, 20)))
    return reqs


def ratio_experiment(trials=1000, n=50, seed=2026):
    rng = random.Random(seed)
    ratios = {"earliest": [], "highest": []}
    for _ in range(trials):
        reqs = random_requests(n, rng)
        opt = best_schedule(reqs)[0]
        ratios["earliest"].append(greedy_earliest_finish(reqs)[0] / opt)
        ratios["highest"].append(greedy_highest_fee(reqs)[0] / opt)
    return ratios


def show(name, reqs):
    print(f"\n{name}: {reqs}")
    for label, f in [("greedy_earliest_finish", greedy_earliest_finish),
                     ("greedy_highest_fee", greedy_highest_fee),
                     ("best_schedule", best_schedule), ("brute_force", brute_force)]:
        print(f"  {label:<23} -> {f(reqs)}")


def plot(ratios):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(7, 3.6))
    bins = [x / 100 for x in range(30, 102, 2)]
    plt.hist(ratios["earliest"], bins=bins, alpha=0.7, label="greedy_earliest_finish")
    plt.hist(ratios["highest"], bins=bins, alpha=0.7, label="greedy_highest_fee")
    plt.axvline(1.0, color="black", ls="--", lw=1, label="optimal (ratio 1.0)")
    plt.xlabel("greedy revenue / optimal revenue")
    plt.ylabel("number of inputs (out of 1,000)")
    plt.title("Revenue ratio, 1,000 random inputs of 50 requests")
    plt.legend(fontsize=8, loc="upper left")
    plt.grid(True, ls=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig("ratio_histogram.png", dpi=150)
    print("\nGraph saved to ratio_histogram.png")


if __name__ == "__main__":
    show("Example from the brief", EXAMPLE)
    show("Counterexample 1 (earliest finish fails)", CE_EARLIEST)
    show("Counterexample 2 (highest fee fails)", CE_HIGHEST)

    ratios = ratio_experiment()
    print("\nRevenue ratio = greedy / optimal, 1,000 random inputs of 50 requests")
    print(f"{'rule':<24}| {'average':>8} | {'worst':>6} | {'optimal in':>10}")
    print("-" * 56)
    for name, label in [("earliest", "greedy_earliest_finish"), ("highest", "greedy_highest_fee")]:
        r = ratios[name]
        hits = sum(1 for x in r if x > 1 - 1e-12)
        print(f"{label:<24}| {sum(r) / len(r):8.3f} | {min(r):6.3f} | {hits:>4} / {len(r)}")
    plot(ratios)
