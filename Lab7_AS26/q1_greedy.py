"""
Lab 7 - Q1: Activity Selection and Knapsack

  select_earliest_finish(acts)   -> greedy by earliest finish (optimal)
  select_earliest_start(acts)    -> greedy by earliest start
  select_shortest(acts)          -> greedy by shortest duration
  fractional_knapsack(items, W)  -> highest value/weight first (optimal)
  greedy_01_knapsack(items, W)   -> same rule, but items cannot be split
  dp_01_knapsack(items, W)       -> dynamic programming (optimal)

Run:  python q1_greedy.py
"""

import random


# ---------------------------------------------------------------------
# Task 1: greedy activity selection (earliest finish time)
# Two activities fit together if one finishes no later than the other starts.
# ---------------------------------------------------------------------
def read_activities(filename):
    """Read one (start, finish) pair per line."""
    with open(filename) as f:
        return [tuple(map(int, line.split())) for line in f if line.strip()]


def greedy_select(acts, key):
    """Sort by the given rule, then accept each activity that does not
    overlap any activity already accepted."""
    chosen = []
    for a in sorted(acts, key=key):
        if all(a[1] <= b[0] or b[1] <= a[0] for b in chosen):
            chosen.append(a)
    return sorted(chosen)


def select_earliest_finish(acts):
    # Sorted by finish, so checking only the last chosen activity is enough: O(n log n)
    chosen, last_finish = [], float("-inf")
    for s, f in sorted(acts, key=lambda a: a[1]):
        if s >= last_finish:
            chosen.append((s, f))
            last_finish = f
    return chosen


# ---------------------------------------------------------------------
# Task 2: two other greedy rules
# ---------------------------------------------------------------------
def select_earliest_start(acts):
    return greedy_select(acts, key=lambda a: a[0])


def select_shortest(acts):
    return greedy_select(acts, key=lambda a: a[1] - a[0])


def random_activities(rng, n):
    acts = []
    for _ in range(n):
        s = rng.randint(0, 20)
        acts.append((s, s + rng.randint(1, 8)))
    return acts


def best_by_brute_force(acts):
    """Largest number of non-overlapping activities, trying every subset."""
    from itertools import combinations
    for size in range(len(acts), 0, -1):
        for sub in combinations(acts, size):
            if all(a[1] <= b[0] or b[1] <= a[0] for a, b in combinations(sub, 2)):
                return size
    return 0


def find_counterexample(rule, rng, trials=10_000):
    """Random testing: look for an input where rule picks fewer activities
    than earliest finish. Returns (first small example found, how many failed)."""
    first, failures = None, 0
    for _ in range(trials):
        acts = random_activities(rng, rng.randint(2, 6))
        if len(rule(acts)) < len(select_earliest_finish(acts)):
            failures += 1
            if first is None or len(acts) < len(first):
                first = acts                          # keep the smallest example
    return first, failures


# ---------------------------------------------------------------------
# Task 3: fractional knapsack (highest value/weight first)
# items are (value, weight)
# ---------------------------------------------------------------------
def fractional_knapsack(items, W):
    total, taken = 0.0, []
    for v, w in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        if W <= 0:
            break
        part = min(1.0, W / w)                        # whole item, or the fraction that fits
        total += v * part
        W -= w * part
        taken.append((v, w, part))
    return total, taken


# ---------------------------------------------------------------------
# Task 4: the same greedy rule on 0/1 knapsack vs DP
# ---------------------------------------------------------------------
def greedy_01_knapsack(items, W):
    total = 0
    for v, w in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        if w <= W:                                    # take the whole item or skip it
            total += v
            W -= w
    return total


def dp_01_knapsack(items, W):
    """best[c] = best value with capacity c using the items seen so far."""
    best = [0] * (W + 1)
    for v, w in items:
        for c in range(W, w - 1, -1):                 # go downwards so each item is used once
            best[c] = max(best[c], best[c - w] + v)
    return best[W]


def knapsack_experiment(trials=10_000, seed=4):
    rng = random.Random(seed)
    ratios, worst = [], None
    for _ in range(trials):
        n = rng.randint(3, 10)
        items = [(rng.randint(1, 100), rng.randint(1, 30)) for _ in range(n)]
        W = rng.randint(10, 60)
        g, opt = greedy_01_knapsack(items, W), dp_01_knapsack(items, W)
        r = g / opt if opt else 1.0
        ratios.append(r)
        if worst is None or r < worst[0]:
            worst = (r, items, W, g, opt)
    return ratios, worst


def plot(ratios):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    plt.figure(figsize=(7, 3.8))
    plt.hist(ratios, bins=[x / 50 for x in range(0, 51)], edgecolor="white")
    plt.axvline(1.0, color="black", ls="--", lw=1, label="optimal (ratio 1.0)")
    plt.yscale("log")
    plt.xlabel("greedy value / optimal value")
    plt.ylabel("number of inputs (log scale)")
    plt.title("0/1 knapsack: greedy by value/weight vs DP, 10,000 random inputs")
    plt.legend()
    plt.grid(True, ls=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig("screenshots/q1_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q1_graph.png")


if __name__ == "__main__":
    acts = read_activities("data/activities.txt")
    print("Task 1: Activities from data/activities.txt:", acts)
    chosen = select_earliest_finish(acts)
    print(f"  earliest finish selects {len(chosen)}: {chosen}")

    print("\nTask 2: Other greedy rules, random testing (10,000 inputs of 2-6 activities)")
    rng = random.Random(2)
    for name, rule in [("earliest start", select_earliest_start), ("shortest duration", select_shortest)]:
        ex, fails = find_counterexample(rule, rng)
        print(f"  {name}: picked fewer than earliest finish on {fails:,} inputs")
        print(f"    smallest counterexample: {ex}")
        print(f"    {name} picks {rule(ex)}, earliest finish picks {select_earliest_finish(ex)}")
    rng = random.Random(3)
    tests = [random_activities(rng, rng.randint(1, 8)) for _ in range(2000)]
    ok = all(len(select_earliest_finish(a)) == best_by_brute_force(a) for a in tests)
    print(f"  earliest finish vs brute force on 2,000 random inputs: always optimal = {ok}")

    print("\nTask 3: Fractional knapsack, items (value, weight) = [(60, 10), (100, 20), (120, 30)], W = 50")
    total, taken = fractional_knapsack([(60, 10), (100, 20), (120, 30)], 50)
    for v, w, part in taken:
        print(f"  take {part:.0%} of item (value {v}, weight {w}, ratio {v / w:.0f})")
    print(f"  total value = {total:.0f}")

    print("\nTask 4: Same greedy rule on 0/1 knapsack vs DP")
    ex = [(60, 10), (100, 20), (120, 30)]
    print(f"  same items, W = 50: greedy = {greedy_01_knapsack(ex, 50)}, DP = {dp_01_knapsack(ex, 50)}")
    ratios, (r, items, W, g, opt) = knapsack_experiment()
    hits = sum(1 for x in ratios if x == 1.0)
    print(f"  10,000 random inputs: greedy optimal on {hits:,}, average ratio {sum(ratios) / len(ratios):.3f}")
    print(f"  worst ratio found = {r:.3f}  (greedy {g}, optimal {opt})")
    print(f"    items = {items}, W = {W}")
    plot(ratios)
