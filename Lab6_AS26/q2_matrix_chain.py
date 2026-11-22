"""
Lab 6 - Q2: Matrix Chain Multiplication

Matrix Ai has size dims[i-1] x dims[i].
  matrix_chain_dp(dims)      -> bottom-up DP: minimum cost and split table    O(n^3)
  parenthesise(split, i, j)  -> optimal order as text, e.g. ((A1(A2A3))A4)
  matrix_chain_brute(dims)   -> tries every parenthesisation recursively      exponential

Run:  python q2_matrix_chain.py
"""

import random


# ---------------------------------------------------------------------
# Task 1: minimum number of scalar multiplications (bottom-up)
# ---------------------------------------------------------------------
def matrix_chain_dp(dims):
    """m[i][j] = min cost of A_i..A_j;  split[i][j] = best k to split at.
    m[i][j] = min over k of  m[i][k] + m[k+1][j] + dims[i-1]*dims[k]*dims[j]."""
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):              # chains of 2, 3, ..., n matrices
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j], split[i][j] = cost, k
    return m[1][n], split


# ---------------------------------------------------------------------
# Task 2: print the optimal parenthesisation
# ---------------------------------------------------------------------
def parenthesise(split, i, j):
    if i == j:
        return f"A{i}"
    k = split[i][j]
    return f"({parenthesise(split, i, k)}{parenthesise(split, k + 1, j)})"


# ---------------------------------------------------------------------
# Task 3: brute-force recursive search (no table)
# ---------------------------------------------------------------------
def matrix_chain_brute(dims, i=1, j=None):
    """Tries every split point at every level."""
    if j is None:
        j = len(dims) - 1
    if i == j:
        return 0
    return min(matrix_chain_brute(dims, i, k) + matrix_chain_brute(dims, k + 1, j)
               + dims[i - 1] * dims[k] * dims[j] for k in range(i, j))


def left_to_right_cost(dims):
    """Cost of (((A1A2)A3)...An): the running result is always dims[0] x dims[k]."""
    return sum(dims[0] * dims[k] * dims[k + 1] for k in range(1, len(dims) - 1))


def report(name, dims):
    best, split = matrix_chain_dp(dims)
    brute = matrix_chain_brute(dims)
    left = left_to_right_cost(dims)
    n = len(dims) - 1
    print(f"\n{name}: dims = {dims}  ({n} matrices)")
    print(f"  optimal order : {parenthesise(split, 1, n)}")
    print(f"  optimal cost  : {best:,}   (brute force: {brute:,}, match: {best == brute})")
    print(f"  left-to-right : {left:,}   ({left / best:.2f}x the optimal cost)")
    return name, n, best, left


def plot(rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    labels = [f"{r[0]}\n({r[1]} matrices)" for r in rows]
    x = range(len(rows))
    plt.figure(figsize=(10, 4))
    plt.bar([i - 0.2 for i in x], [r[3] for r in rows], width=0.4, label="left-to-right order")
    plt.bar([i + 0.2 for i in x], [r[2] for r in rows], width=0.4, label="optimal order (DP)")
    plt.yscale("log")
    plt.xticks(list(x), labels, fontsize=8)
    plt.ylabel("scalar multiplications (log scale)")
    plt.title("Matrix chain: left-to-right cost vs optimal cost")
    plt.grid(True, axis="y", which="both", ls=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("screenshots/q2_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q2_graph.png")


if __name__ == "__main__":
    rows = [report("Chain 1", [30, 35, 15, 5, 10, 20, 25]),
            report("Chain 2", [5, 4, 6, 2, 7])]
    rng = random.Random(6)
    for t in range(1, 6):                        # 5 random chains of 3 to 8 matrices
        n = rng.randint(3, 8)
        rows.append(report(f"Random {t}", [rng.randint(2, 50) for _ in range(n + 1)]))
    plot(rows)
