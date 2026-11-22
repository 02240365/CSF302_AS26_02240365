"""
Lab 4 - Part A: Efficient Modular Exponentiation

Calculates a^b mod m in three ways:
  naive_mod_exp         -> repeated multiplication, b steps         O(b)
  binary_mod_exp        -> square-and-multiply with % 2 and // 2    O(log b)
  binary_mod_exp_bitwise-> same idea using b & 1 and b >>= 1        O(log b)

Run:  python modular_exponentiation.py
"""

import time


# ---------------------------------------------------------------------
# Task 5: input validation (used by every function below)
# ---------------------------------------------------------------------
def validate(a, b, m):
    """Check the inputs and return the base reduced into the range 0..m-1."""
    if m < 1:
        raise ValueError("modulus m must be at least 1")
    if b < 0:
        raise ValueError("exponent b must not be negative")
    return a % m          # a negative base becomes positive, e.g. -2 mod 7 = 5


# ---------------------------------------------------------------------
# Task 1: naive modular exponentiation (repeated multiplication)
# ---------------------------------------------------------------------
def naive_mod_exp(a, b, m):
    a = validate(a, b, m)
    result = 1 % m        # b = 0 gives 1 mod m (which is 0 when m = 1)
    for _ in range(b):
        result = (result * a) % m     # reduce every step so numbers stay small
    return result


# ---------------------------------------------------------------------
# Task 2: binary exponentiation (square-and-multiply)
# ---------------------------------------------------------------------
def binary_mod_exp(a, b, m):
    a = validate(a, b, m)
    result = 1 % m
    while b > 0:
        if b % 2 == 1:                # odd exponent: multiply this power in
            result = (result * a) % m
        a = (a * a) % m               # square the base
        b = b // 2                    # halve the exponent
    return result


# ---------------------------------------------------------------------
# Task 4: binary exponentiation with bitwise operations
# ---------------------------------------------------------------------
def binary_mod_exp_bitwise(a, b, m):
    a = validate(a, b, m)
    result = 1 % m
    while b:
        if b & 1:                     # last bit is 1 -> exponent is odd
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1                       # shift right = halve the exponent
    return result


# ---------------------------------------------------------------------
# Helpers for printing and timing
# ---------------------------------------------------------------------
def best_time(func, *args, repeats=3):
    """Smallest time of a few runs (one run if it is slow)."""
    best = None
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
        if t > 0.5:
            break
    return best


def task3_compare():
    print("\nTask 3 & 4: Compare naive, binary and bitwise results")
    tests = [(2, 10, 1000), (3, 200, 13), (7, 128, 10**9 + 7), (5, 0, 13),
             (123456789, 1000, 998244353), (10, 25, 1), (-2, 5, 7), (2, 64, 2**61 - 1)]
    print(f"{'a':>10} {'b':>5} {'m':>19} | {'naive':>10} {'binary':>10} {'bitwise':>10} | match")
    print("-" * 83)
    for a, b, m in tests:
        n, bi, bw = naive_mod_exp(a, b, m), binary_mod_exp(a, b, m), binary_mod_exp_bitwise(a, b, m)
        ok = n == bi == bw == pow(a, b, m)          # Python's pow() as a final check
        print(f"{a:>10} {b:>5} {m:>19} | {n:>10} {bi:>10} {bw:>10} | {ok}")


def task5_validation():
    print("\nTask 5: Input validation")
    print(f"  zero exponent     2^0 mod 7      = {binary_mod_exp(2, 0, 7)}   (1 mod 7)")
    print(f"  zero exponent     2^0 mod 1      = {binary_mod_exp(2, 0, 1)}   (1 mod 1)")
    print(f"  negative base    (-2)^5 mod 7    = {binary_mod_exp(-2, 5, 7)}   (-2 is reduced to 5 first)")
    for label, args in [("negative exponent  2^-3 mod 7  ", (2, -3, 7)),
                        ("invalid modulus    2^5 mod 0   ", (2, 5, 0))]:
        try:
            binary_mod_exp(*args)
        except ValueError as e:
            print(f"  {label} -> ValueError: {e}")


def task6_timing():
    print("\nTask 6: Execution time (a = 123456789, m = 10^9 + 7)")
    a, m = 123456789, 10**9 + 7
    bs = [10**k for k in range(1, 7)]
    rows = []
    print(f"{'b':>9} | {'naive (ms)':>11} | {'binary (ms)':>11} | {'bitwise (ms)':>12} | {'naive / binary':>14}")
    print("-" * 70)
    for b in bs:
        tn = best_time(naive_mod_exp, a, b, m)
        tb = best_time(binary_mod_exp, a, b, m, repeats=20)
        tw = best_time(binary_mod_exp_bitwise, a, b, m, repeats=20)
        rows.append((b, tn, tb, tw))
        print(f"{b:>9} | {tn*1000:>11.4f} | {tb*1000:>11.4f} | {tw*1000:>12.4f} | {tn/tb:>13.0f}x")
    return rows


def plot(rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    bs = [r[0] for r in rows]
    plt.figure(figsize=(7, 4.2))
    plt.loglog(bs, [r[1] for r in rows], "o-", label="naive  O(b)")
    plt.loglog(bs, [r[2] for r in rows], "s-", label="binary  O(log b)")
    plt.loglog(bs, [r[3] for r in rows], "^--", label="binary bitwise  O(log b)")
    plt.xlabel("exponent b (log scale)")
    plt.ylabel("time in seconds (log scale)")
    plt.title("Modular exponentiation: naive vs binary")
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("screenshots/partA_graph.png", dpi=150)
    print("\nGraph saved to screenshots/partA_graph.png")


if __name__ == "__main__":
    print("Task 1 & 2: 3^13 mod 7")
    print(f"  naive  = {naive_mod_exp(3, 13, 7)}")
    print(f"  binary = {binary_mod_exp(3, 13, 7)}")
    task3_compare()
    task5_validation()
    plot(task6_timing())
