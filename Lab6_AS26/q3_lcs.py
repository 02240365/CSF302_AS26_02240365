"""
Lab 6 - Q3: Longest Common Subsequence

  lcs_table(X, Y)          -> fills the full table bottom-up             O(mn) time, O(mn) space
  lcs_reconstruct(...)     -> walks back through the table to get one LCS
  lcs_length_two_rows(X,Y) -> length only, keeping just two rows          O(mn) time, O(n) space
  lcs_brute(X, Y)          -> tries all 2^m subsequences of X             O(2^m * n)
  diff(old, new)           -> line-by-line diff of two text files using LCS

Run:  python q3_lcs.py      (about 10 seconds)
"""

import random
import time
from itertools import combinations


# ---------------------------------------------------------------------
# Task 1: fill the LCS table bottom-up
# ---------------------------------------------------------------------
def lcs_table(X, Y):
    """c[i][j] = length of an LCS of X[:i] and Y[:j]."""
    m, n = len(X), len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1          # match: extend the diagonal
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])  # skip one item from X or Y
    return c


def print_table(X, Y, c):
    print("      " + "  ".join(f"{ch:>2}" for ch in " " + Y))
    for i in range(len(X) + 1):
        label = X[i - 1] if i > 0 else " "
        print(f"  {label:>2}  " + "  ".join(f"{v:>2}" for v in c[i]))


# ---------------------------------------------------------------------
# Task 2: reconstruct one LCS
# ---------------------------------------------------------------------
def lcs_reconstruct(X, Y, c):
    i, j, out = len(X), len(Y), []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            out.append(X[i - 1]); i -= 1; j -= 1     # part of the LCS
        elif c[i - 1][j] >= c[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return out[::-1]


def lcs(X, Y):
    return lcs_reconstruct(X, Y, lcs_table(X, Y))


# ---------------------------------------------------------------------
# Task 3: space-optimised length (two rows only)
# ---------------------------------------------------------------------
def lcs_length_two_rows(X, Y):
    prev = [0] * (len(Y) + 1)
    for i in range(1, len(X) + 1):
        cur = [0] * (len(Y) + 1)
        for j in range(1, len(Y) + 1):
            if X[i - 1] == Y[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur                                   # the older row is thrown away
    return prev[-1]


# ---------------------------------------------------------------------
# Task 4: brute force (every subsequence of X)
# ---------------------------------------------------------------------
def is_subsequence(s, Y):
    it = iter(Y)
    return all(ch in it for ch in s)                 # each 'in' moves forward through Y


def lcs_brute(X, Y):
    """Try all 2^m subsequences of X (one for each subset of positions)
    and keep the longest one that is also a subsequence of Y."""
    best, tried = 0, 0
    for size in range(len(X) + 1):
        for idx in combinations(range(len(X)), size):
            tried += 1
            if size > best and is_subsequence([X[i] for i in idx], Y):
                best = size
    return best, tried


def best_of_3(func, *args):
    """Run 3 times and keep the fastest time (less noise from other programs)."""
    best = None
    for _ in range(3):
        start = time.perf_counter()
        result = func(*args)
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
    return result, best


def task4_timing():
    print("\nTask 4: DP vs brute force on random strings over A, C, G, T (time in ms)")
    rng = random.Random(4)
    rows = []
    print(f"{'length':>6} | {'LCS':>3} | {'DP ms':>8} | {'brute ms':>10} | {'subsequences tried (2^m)':>24}")
    print("-" * 62)
    for m in range(5, 19):
        X = "".join(rng.choice("ACGT") for _ in range(m))
        Y = "".join(rng.choice("ACGT") for _ in range(m))
        d, td = best_of_3(lcs_length_two_rows, X, Y)
        (b, tried), tb = best_of_3(lcs_brute, X, Y)
        assert d == b == len(lcs(X, Y))
        rows.append((m, td, tb))
        print(f"{m:>6} | {d:>3} | {td*1000:>8.3f} | {tb*1000:>10.3f} | {tried:>24,}")
    return rows


# ---------------------------------------------------------------------
# Task 5: line-by-line diff of two text files
# ---------------------------------------------------------------------
def diff(old_lines, new_lines):
    """Lines in the LCS are unchanged ('  '), others are removed ('- ') or added ('+ ')."""
    c = lcs_table(old_lines, new_lines)
    i, j, out = len(old_lines), len(new_lines), []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_lines[i - 1] == new_lines[j - 1]:
            out.append("  " + old_lines[i - 1]); i -= 1; j -= 1
        elif j > 0 and (i == 0 or c[i][j - 1] >= c[i - 1][j]):
            out.append("+ " + new_lines[j - 1]); j -= 1
        else:
            out.append("- " + old_lines[i - 1]); i -= 1
    return out[::-1]


def task5_diff(old_file="old.txt", new_file="new.txt"):
    print(f"\nTask 5: Line-by-line diff of {old_file} and {new_file}")
    with open(old_file) as f:
        old = f.read().splitlines()
    with open(new_file) as f:
        new = f.read().splitlines()
    for line in diff(old, new):
        print("  " + line)
    print(f"  ({len(lcs(old, new))} lines unchanged, "
          f"{len(old) - len(lcs(old, new))} removed, {len(new) - len(lcs(old, new))} added)")


def plot(rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    ms = [r[0] for r in rows]
    plt.figure(figsize=(7, 4.2))
    plt.semilogy(ms, [r[2] for r in rows], "o-", label="brute force  O(2^m · n)")
    plt.semilogy(ms, [r[1] for r in rows], "s-", label="DP  O(m · n)")
    plt.xlabel("string length (m = n)")
    plt.ylabel("time in seconds (log scale)")
    plt.title("LCS: DP vs brute force")
    plt.xticks(ms)
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("screenshots/q3_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q3_graph.png")


if __name__ == "__main__":
    X, Y = "ABCBDAB", "BDCABA"
    print(f"Task 1: LCS table for X = {X}, Y = {Y}")
    c = lcs_table(X, Y)
    print_table(X, Y, c)
    print(f"\nTask 2: one LCS = {''.join(lcs_reconstruct(X, Y, c))}  (length {c[-1][-1]})")
    print(f"Task 3: length with two rows only = {lcs_length_two_rows(X, Y)}")
    plot(task4_timing())
    task5_diff()
