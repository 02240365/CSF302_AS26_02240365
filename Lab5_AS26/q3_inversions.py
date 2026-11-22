"""
Lab 5 - Q3: Counting Inversions

An inversion is a pair i < j with a[i] > a[j].
  count_inversions_brute(a)   -> checks every pair                  O(n^2)
  count_inversions_merge(a)   -> counts while merge sorting         O(n log n)
Then uses it to find the Kendall tau distance between two users'
rankings of 10 movies, typed in from the keyboard.

Run:  python q3_inversions.py      (takes about 2 minutes before asking for input)
"""

import random
import time

TIME_LIMIT = 60.0          # stop brute force after 60 seconds


class TooSlow(Exception):
    pass


# ---------------------------------------------------------------------
# Task 1: brute force, check every pair
# ---------------------------------------------------------------------
def count_inversions_brute(a, time_limit=None):
    start = time.perf_counter()
    n, count = len(a), 0
    for i in range(n):
        x = a[i]
        for j in range(i + 1, n):
            if x > a[j]:
                count += 1
        if time_limit and i % 100 == 0 and time.perf_counter() - start > time_limit:
            raise TooSlow                 # gave up: over the time limit
    return count


# ---------------------------------------------------------------------
# Task 2: merge-sort-based count
# ---------------------------------------------------------------------
def count_inversions_merge(a):
    """Returns the number of inversions (a is not changed)."""
    return _sort_count(list(a))[1]


def _sort_count(a):
    """Returns (sorted copy of a, number of inversions in a)."""
    if len(a) <= 1:
        return a, 0
    mid = len(a) // 2
    left, inv_left = _sort_count(a[:mid])
    right, inv_right = _sort_count(a[mid:])
    merged, i, j, split = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            # right[j] is smaller than left[i] AND every item after left[i],
            # so it forms an inversion with all len(left) - i of them
            merged.append(right[j]); j += 1
            split += len(left) - i
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv_left + inv_right + split


# ---------------------------------------------------------------------
# Task 3: both give the same answer on random arrays up to size 2,000
# ---------------------------------------------------------------------
def task3_verify():
    print("Task 3: Brute force vs merge sort on random arrays of size 0 to 2,000")
    rng = random.Random(3)
    sizes = [0, 1, 2, 10, 100, 500, 1000, 2000] + [rng.randint(0, 2000) for _ in range(42)]
    for n in sizes:
        a = [rng.randint(0, 1000) for _ in range(n)]       # includes repeated values
        assert count_inversions_brute(a) == count_inversions_merge(a), f"mismatch at n={n}"
    print(f"  {len(sizes)} random arrays tested: all match")
    print(f"  sorted [1..5]         -> {count_inversions_merge([1, 2, 3, 4, 5])} inversions (minimum)")
    print(f"  reverse [5..1]        -> {count_inversions_merge([5, 4, 3, 2, 1])} inversions (maximum = 5*4/2)")
    print(f"  [2, 4, 1, 3, 5]       -> {count_inversions_merge([2, 4, 1, 3, 5])} inversions: (2,1) (4,1) (4,3)")


# ---------------------------------------------------------------------
# Task 4: timing, n = 1,000 to 1,000,000
# ---------------------------------------------------------------------
def task4_timing():
    print(f"\nTask 4: Time in seconds (brute force is stopped after {TIME_LIMIT:.0f} s)")
    rng = random.Random(4)
    sizes = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
    rows, brute_stopped = [], False
    print(f"{'n':>10} | {'brute force':>14} | {'merge sort':>10} | {'inversions':>16}")
    print("-" * 61)
    for n in sizes:
        a = [rng.randint(0, 10**9) for _ in range(n)]
        start = time.perf_counter()
        inv = count_inversions_merge(a)
        tm = time.perf_counter() - start

        if brute_stopped:
            tb, text = None, "skipped"
        else:
            try:
                start = time.perf_counter()
                assert count_inversions_brute(a, TIME_LIMIT) == inv
                tb = time.perf_counter() - start
                text = f"{tb:.3f}"
            except TooSlow:
                tb, text, brute_stopped = None, "> 60 (stopped)", True
        rows.append((n, tb, tm))
        print(f"{n:>10,} | {text:>14} | {tm:>10.3f} | {inv:>16,}")
    return rows


def plot(rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    plt.figure(figsize=(7, 4.2))
    bn = [r[0] for r in rows if r[1] is not None]
    plt.loglog(bn, [r[1] for r in rows if r[1] is not None], "o-", label="brute force  O(n²)")
    plt.loglog([r[0] for r in rows], [r[2] for r in rows], "s-", label="merge sort  O(n log n)")
    plt.axhline(TIME_LIMIT, color="grey", ls="--", lw=1, label="60 s limit")
    plt.xlabel("n (log scale)")
    plt.ylabel("time in seconds (log scale)")
    plt.title("Counting inversions: brute force vs merge sort")
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("screenshots/q3_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q3_graph.png")


# ---------------------------------------------------------------------
# Task 5: Kendall tau distance between two users' movie rankings
# ---------------------------------------------------------------------
MOVIES = ["Inception", "Titanic", "Avatar", "Interstellar", "Frozen",
          "Coco", "Up", "Joker", "Parasite", "Jaws"]


def read_ranking(user):
    """Ask for a ranking: the 10 movie numbers from favourite to least favourite."""
    while True:
        text = input(f"  {user}, enter your ranking (10 movie numbers, best first): ")
        try:
            ranking = [int(x) for x in text.replace(",", " ").split()]
        except ValueError:
            print("    Please type numbers only.")
            continue
        if sorted(ranking) == list(range(1, 11)):
            return ranking
        print("    Please use each number from 1 to 10 exactly once.")


def kendall_tau_distance(rank_a, rank_b):
    """Number of movie pairs the two users put in a different order.
    Write user B's position of each movie in user A's order;
    every inversion in that list is a pair they disagree on."""
    position_b = {movie: pos for pos, movie in enumerate(rank_b)}
    return count_inversions_merge([position_b[movie] for movie in rank_a])


def task5_kendall_tau():
    print("\nTask 5: Kendall tau distance between two users' movie rankings")
    for i, m in enumerate(MOVIES, 1):
        print(f"  {i:>2}. {m}")
    a = read_ranking("User 1")
    b = read_ranking("User 2")
    d = kendall_tau_distance(a, b)
    pairs = len(MOVIES) * (len(MOVIES) - 1) // 2          # 45 pairs of movies
    print(f"\n  User 1: {' > '.join(MOVIES[m - 1] for m in a)}")
    print(f"  User 2: {' > '.join(MOVIES[m - 1] for m in b)}")
    print(f"  Kendall tau distance = {d} of {pairs} pairs are in a different order")
    print(f"  Similarity = 1 - {d}/{pairs} = {1 - d / pairs:.2f}   (1 = same ranking, 0 = opposite)")


if __name__ == "__main__":
    task3_verify()
    plot(task4_timing())
    task5_kendall_tau()
