"""
CSF302 Assignment 2: Closest Camera Traps

Finds the closest pair of camera traps on a map grid.
  closest_pair_brute(points) -> checks every pair, Theta(n^2)
  closest_pair(points)       -> divide and conquer, Theta(n log n)
Both return (d, i, j): smallest distance d and indices i < j of the two points.

Run "python closest.py" to do the timing experiment (Part C).
"""

import math


def dist(p, q):
    """Euclidean distance between two points (x, y)."""
    return math.hypot(p[0] - q[0], p[1] - q[1])


def ordered(d, a, b):
    """Return (d, i, j) with the smaller index first so that i < j."""
    return (d, a, b) if a < b else (d, b, a)


# ---------------------------------------------------------------------
# Part A.1  Brute force: Theta(n^2)
# ---------------------------------------------------------------------
def closest_pair_brute(points):
    """Compare every pair of points and keep the closest one."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")

    best = (math.inf, -1, -1)
    for i in range(n - 1):
        for j in range(i + 1, n):          # j > i, so each pair is checked once
            d = dist(points[i], points[j])
            if d < best[0]:
                best = (d, i, j)
    return best


# ---------------------------------------------------------------------
# Part A.2  Divide and conquer: Theta(n log n)
# ---------------------------------------------------------------------
def closest_pair(points):
    """
    Divide and conquer closest pair.
      1. Sort point indices by x once (and by y once).
      2. Split at the middle x, solve the left and right halves.
      3. delta = smaller of the two answers.
      4. Check the strip of width 2*delta around the dividing line.
    """
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")

    # We work with indices so we can report the original positions i, j.
    by_x = sorted(range(n), key=lambda k: (points[k][0], points[k][1]))
    by_y = sorted(range(n), key=lambda k: (points[k][1], points[k][0]))

    d, i, j = _solve(points, by_x, by_y)
    return ordered(d, i, j)


def _solve(pts, by_x, by_y):
    """Recursive helper. by_x and by_y hold the SAME indices,
    sorted by x and by y respectively."""
    n = len(by_x)

    # Base case: 3 or fewer points -> just check every pair.
    if n <= 3:
        best = (math.inf, -1, -1)
        for a in range(n):
            for b in range(a + 1, n):
                d = dist(pts[by_x[a]], pts[by_x[b]])
                if d < best[0]:
                    best = (d, by_x[a], by_x[b])
        return best

    # DIVIDE: split the x-sorted list in the middle.
    mid = n // 2
    mid_x = pts[by_x[mid]][0]              # x of the dividing line
    left_x, right_x = by_x[:mid], by_x[mid:]

    # Split the y-sorted list into the same two halves, keeping y order.
    # (Using a set of indices handles duplicate x values correctly.)
    left_set = set(left_x)
    left_y = [k for k in by_y if k in left_set]
    right_y = [k for k in by_y if k not in left_set]

    # CONQUER: solve each half recursively.
    best = min(_solve(pts, left_x, left_y), _solve(pts, right_x, right_y))
    delta = best[0]

    # COMBINE: points within delta of the dividing line (strip width 2*delta),
    # already in y order because by_y is sorted by y.
    strip = [k for k in by_y if abs(pts[k][0] - mid_x) < delta]

    # Each strip point only needs to be compared with the next few points
    # above it (at most 7), so this loop is O(n).
    for a in range(len(strip)):
        for b in range(a + 1, len(strip)):
            if pts[strip[b]][1] - pts[strip[a]][1] >= best[0]:
                break                       # too far up, stop early
            d = dist(pts[strip[a]], pts[strip[b]])
            if d < best[0]:
                best = (d, strip[a], strip[b])
    return best


# ---------------------------------------------------------------------
# Part C  Timing experiment
# ---------------------------------------------------------------------
def time_once(func, points):
    """Run func(points) once and return the time taken in seconds."""
    import time
    start = time.perf_counter()
    func(points)
    return time.perf_counter() - start


def best_time(func, points, repeats=5):
    """Smallest of several runs (reduces noise for small inputs)."""
    return min(time_once(func, points) for _ in range(repeats))


def random_points(n, seed):
    """n random points on a large integer map grid."""
    import random
    rng = random.Random(seed)
    return [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(n)]


def run_timing():
    import sys
    sys.setrecursionlimit(10000)
    LIMIT = 60.0                                  # stop brute force after 60 s
    sizes = [1000 * 2**k for k in range(7)]       # 1,000 ... 64,000

    rows = []
    brute_stopped = False
    print(f"{'n':>8} | {'brute (s)':>12} | {'D&C (s)':>10} | {'speed-up':>8}")
    print("-" * 48)
    for n in sizes:
        pts = random_points(n, seed=n)
        t_dc = best_time(closest_pair, pts, repeats=3)   # best of 3 (fast, so cheap)

        if brute_stopped:
            t_brute = None                        # skipped
        else:
            t_brute = time_once(closest_pair_brute, pts)
            if t_brute > LIMIT:
                brute_stopped = True              # don't run larger n

        b_txt = f"{t_brute:12.3f}" if t_brute is not None else f"{'skipped>60s':>12}"
        s_txt = f"{t_brute / t_dc:7.0f}x" if t_brute is not None else f"{'-':>8}"
        print(f"{n:>8} | {b_txt} | {t_dc:10.4f} | {s_txt}")
        rows.append((n, t_brute, t_dc))

    # Crossover: smallest n where divide and conquer beats brute force.
    print("\nCrossover search (best of 5 runs, averaged over 20 inputs):")
    crossover = None
    for n in range(2, 301):
        tb = td = 0.0
        for s in range(20):
            pts = random_points(n, seed=1000 * n + s)
            tb += best_time(closest_pair_brute, pts)
            td += best_time(closest_pair, pts)
        if td < tb:
            crossover = n
            break
    print(f"Smallest n where D&C is faster: n = {crossover}")
    for n in range(max(2, crossover - 4), crossover + 5):
        tb = sum(best_time(closest_pair_brute, random_points(n, 7 * n + s)) for s in range(20)) / 20
        td = sum(best_time(closest_pair, random_points(n, 7 * n + s)) for s in range(20)) / 20
        print(f"  n={n:>3}: brute {tb * 1e6:8.1f} us   D&C {td * 1e6:8.1f} us")

    plot(rows)
    return rows, crossover


def plot(rows):
    """Save a labelled log-log graph of the timing results."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ns = [r[0] for r in rows]
    dc = [r[2] for r in rows]
    bn = [r[0] for r in rows if r[1] is not None]
    bt = [r[1] for r in rows if r[1] is not None]

    plt.figure(figsize=(7, 4.5))
    plt.loglog(bn, bt, "o-", label="Brute force  Θ(n²)")
    plt.loglog(ns, dc, "s-", label="Divide and conquer  Θ(n log n)")
    plt.axhline(60, color="grey", ls="--", lw=1, label="60 s limit")
    plt.xlabel("Number of camera traps n (log scale)")
    plt.ylabel("Running time in seconds (log scale)")
    plt.title("Closest pair: brute force vs divide and conquer")
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("timing_loglog.png", dpi=150)
    print("Graph saved to timing_loglog.png")


if __name__ == "__main__":
    # Quick example from the assignment sheet.
    example = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("Example brute :", closest_pair_brute(example))
    print("Example D&C   :", closest_pair(example), "\n")
    run_timing()
