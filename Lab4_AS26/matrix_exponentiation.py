"""
Lab 4 - Part B: Efficient Matrix Modular Exponentiation

Calculates A^n mod m for a square matrix A:
  naive_mat_pow   -> n matrix multiplications           O(n * d^3)
  binary_mat_pow  -> repeated squaring                  O(log n * d^3)
Then uses it for Fibonacci numbers and for counting walks in a graph.

Run:  python matrix_exponentiation.py
"""

import random
import time


# ---------------------------------------------------------------------
# Task 1: multiply two square matrices, reducing every element mod m
# ---------------------------------------------------------------------
def mat_mult(A, B, m):
    cols = list(zip(*B))                       # columns of B
    return [[sum(x * y for x, y in zip(row, col)) % m for col in cols] for row in A]


# ---------------------------------------------------------------------
# Task 2: identity matrix of size d
# ---------------------------------------------------------------------
def identity(d):
    return [[1 if i == j else 0 for j in range(d)] for i in range(d)]


def validate(A, n, m):
    if m < 1:
        raise ValueError("modulus m must be at least 1")
    if n < 0:
        raise ValueError("exponent n must not be negative")
    if any(len(row) != len(A) for row in A):
        raise ValueError("matrix must be square")


# ---------------------------------------------------------------------
# Task 3: naive matrix exponentiation (n multiplications)
# ---------------------------------------------------------------------
def naive_mat_pow(A, n, m):
    validate(A, n, m)
    A = [[x % m for x in row] for row in A]
    result = [[x % m for x in row] for row in identity(len(A))]   # A^0 = I (mod m)
    for _ in range(n):
        result = mat_mult(result, A, m)
    return result


# ---------------------------------------------------------------------
# Task 4: binary matrix exponentiation (repeated squaring)
# ---------------------------------------------------------------------
def binary_mat_pow(A, n, m):
    validate(A, n, m)
    A = [[x % m for x in row] for row in A]
    result = [[x % m for x in row] for row in identity(len(A))]
    while n:
        if n & 1:                          # odd: multiply this power in
            result = mat_mult(result, A, m)
        A = mat_mult(A, A, m)              # square
        n >>= 1                            # halve
    return result


# ---------------------------------------------------------------------
# Task 6 & 7: Fibonacci numbers mod m
# ---------------------------------------------------------------------
def fib_mod(n, m):
    """[[1,1],[1,0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]], so F(n) is the top-right."""
    return binary_mat_pow([[1, 1], [1, 0]], n, m)[0][1]


def fib_iterative(n, m):
    """Slow check: build F(0), F(1), ..., F(n) one by one."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % m
    return a


def fib_fast_doubling(n, m):
    """A different fast method, used only to double-check F(10^18):
    F(2k) = F(k)(2F(k+1) - F(k)),  F(2k+1) = F(k)^2 + F(k+1)^2."""
    def fd(k):
        if k == 0:
            return 0, 1
        f, g = fd(k >> 1)
        c = f * ((2 * g - f) % m) % m
        d = (f * f + g * g) % m
        return (d, (c + d) % m) if k & 1 else (c, d)
    return fd(n)[0]


# ---------------------------------------------------------------------
# Task 8: number of walks of exactly k edges from u to v
# ---------------------------------------------------------------------
def count_walks(adj, u, v, k, m):
    """Entry (u, v) of adj^k counts the walks of length k from u to v."""
    return binary_mat_pow(adj, k, m)[u][v]


def count_walks_brute(adj, u, v, k):
    """Slow check: follow every possible walk step by step."""
    if k == 0:
        return 1 if u == v else 0
    return sum(count_walks_brute(adj, w, v, k - 1) for w in range(len(adj)) if adj[u][w])


# ---------------------------------------------------------------------
# Printing helpers
# ---------------------------------------------------------------------
def task5_compare():
    print("\nTask 5: Compare naive and binary matrix exponentiation")
    rng = random.Random(4)
    cases = [([[1, 1], [1, 0]], 10, 1000), ([[2, 3], [1, 4]], 25, 97),
             ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 50, 10**9 + 7), ([[5, 7], [3, 2]], 0, 11),
             ([[-1, 2], [3, -4]], 13, 1000), ([[9, 9], [9, 9]], 7, 1)]
    cases.append(([[rng.randint(0, 99) for _ in range(4)] for _ in range(4)], 100, 12345))
    for A, n, m in cases:
        same = naive_mat_pow(A, n, m) == binary_mat_pow(A, n, m)
        print(f"  d={len(A)}  n={n:<3}  m={m:<10}  A={str(A) if len(A) < 4 else '4x4 random'}  ->  same result: {same}")
    print("  Example: [[2,3],[1,4]]^25 mod 97 =", binary_mat_pow([[2, 3], [1, 4]], 25, 97))


def task6_fibonacci():
    print("\nTask 6: Fibonacci numbers mod m using matrix exponentiation")
    for n, m in [(10, 10**9), (50, 10**9), (90, 10**9 + 7), (1000, 1000), (5000, 10**9 + 7)]:
        f, check = fib_mod(n, m), fib_iterative(n, m)
        print(f"  F({n}) mod {m} = {f}   (step-by-step check: {check}, match: {f == check})")


def task7_big_fibonacci():
    print("\nTask 7: F(10^18) mod (10^9 + 7)")
    n, m = 10**18, 10**9 + 7
    start = time.perf_counter()
    f = fib_mod(n, m)
    t = time.perf_counter() - start
    print(f"  F(10^18) mod (10^9 + 7) = {f}")
    print(f"  time: {t*1000:.3f} ms, using only about {2 * n.bit_length()} matrix multiplications")
    print(f"  double-check with fast doubling: {fib_fast_doubling(n, m)}, match: {f == fib_fast_doubling(n, m)}")


def task8_walks():
    print("\nTask 8: Walks of exactly k edges in a directed graph")
    #       0 -> 1, 0 -> 2, 1 -> 2, 2 -> 0, 2 -> 3, 3 -> 1
    adj = [[0, 1, 1, 0],
           [0, 0, 1, 0],
           [1, 0, 0, 1],
           [0, 1, 0, 0]]
    print("  Edges: 0->1, 0->2, 1->2, 2->0, 2->3, 3->1")
    for u, v, k in [(0, 3, 2), (0, 0, 3), (0, 2, 5), (1, 1, 6), (0, 3, 10)]:
        w, b = count_walks(adj, u, v, k, 10**9 + 7), count_walks_brute(adj, u, v, k)
        print(f"  walks {u} -> {v} with k = {k:<2}: {w:<4} (brute-force check: {b}, match: {w == b})")
    print(f"  walks 0 -> 3 with k = 10^15 (mod 10^9 + 7): {count_walks(adj, 0, 3, 10**15, 10**9 + 7)}")


def task9_benchmark():
    print("\nTask 9: Benchmark (random d x d matrix, m = 10^9 + 7)")
    m = 10**9 + 7
    dims = [2, 4, 8, 16, 32]
    exps = [2**k for k in range(4, 13)]
    rng = random.Random(9)
    results = {}
    for d in dims:
        A = [[rng.randint(0, m - 1) for _ in range(d)] for _ in range(d)]
        for n in exps:
            results[(d, n)] = (timed(naive_mat_pow, A, n, m), timed(binary_mat_pow, A, n, m))

    for k, name in [(0, "Naive"), (1, "Binary")]:
        print(f"\n  {name} time (ms)")
        print("  " + f"{'n':>6} |" + "".join(f"{'d = ' + str(d):>11}" for d in dims))
        print("  " + "-" * 64)
        for n in exps:
            print("  " + f"{n:>6} |" + "".join(f"{results[(d, n)][k]*1000:>11.3f}" for d in dims))
    print(f"\n  Speed-up (naive / binary) at n = {exps[-1]}:  " +
          ",  ".join(f"d={d}: {results[(d, exps[-1])][0] / results[(d, exps[-1])][1]:.0f}x" for d in dims))
    return dims, exps, results


def timed(func, *args):
    best = None
    for _ in range(3):
        start = time.perf_counter()
        func(*args)
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
        if t > 0.2:            # slow run: one measurement is enough
            break
    return best


def plot(dims, exps, results):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for d in dims:
        axes[0].loglog(exps, [results[(d, n)][0] for n in exps], "o-", label=f"d = {d}")
        axes[1].loglog(exps, [results[(d, n)][1] for n in exps], "s-", label=f"d = {d}")
    axes[0].set_title("Naive  O(n · d³)")
    axes[1].set_title("Binary  O(log n · d³)")
    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_xlabel("exponent n (log scale)")
        ax.grid(True, which="both", ls=":", alpha=0.6)
        ax.legend(fontsize=8)
    axes[0].set_ylabel("time in seconds (log scale)")
    plt.suptitle("Matrix exponentiation: naive vs binary")
    plt.tight_layout()
    plt.savefig("screenshots/partB_graph.png", dpi=150)
    print("\nGraph saved to screenshots/partB_graph.png")


if __name__ == "__main__":
    print("Task 1 & 2: [[1,2],[3,4]] x [[5,6],[7,8]] mod 10 and the 3x3 identity")
    print("  product :", mat_mult([[1, 2], [3, 4]], [[5, 6], [7, 8]], 10))
    print("  identity:", identity(3))
    print("\nTask 3 & 4: [[1,1],[1,0]]^10 mod 1000")
    print("  naive :", naive_mat_pow([[1, 1], [1, 0]], 10, 1000))
    print("  binary:", binary_mat_pow([[1, 1], [1, 0]], 10, 1000))
    task5_compare()
    task6_fibonacci()
    task7_big_fibonacci()
    task8_walks()
    plot(*task9_benchmark())
