"""
CSF302 - Lab 3
Q1: Matrix Multiplication - Strassen's vs Traditional

WHAT THIS PROGRAM DOES
-----------------------
1. Generates two random n x n matrices (n is always a power of 2).
2. Multiplies them using:
      (a) Traditional Method   -> triple nested loop        -> O(n^3)
      (b) Strassen's Algorithm -> divide and conquer, 7 sub -> O(n^2.81)
                                   multiplications per split
3. Displays the resultant matrices from both methods and verifies
   that they match (element by element).
4. Counts the number of basic operations (multiplications + additions)
   performed by each method (step/frequency count).
5. Times both methods on increasing matrix sizes and prints a
   comparison table, then plots a graph (time vs n).

Student No: 02240365
"""

import random
import time
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# STEP COUNTER
# A simple global-style counter object so both algorithms can record
# every basic operation (multiplication / addition / subtraction) the
# same way. Using a small class keeps the counting logic in one place.
# ---------------------------------------------------------------------
class StepCounter365:
    def __init__(self):
        self.count = 0

    def add(self, n=1):
        self.count += n


# ---------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------
def random_matrix_365(n, low=0, high=9):
    """Create an n x n matrix filled with random small integers."""
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def print_matrix_365(M, label=""):
    """Pretty-print a matrix with an optional label."""
    if label:
        print(label)
    for row in M:
        print(row)
    print()


def matrices_equal_365(A, B):
    """Return True if two matrices are identical, element by element."""
    n = len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] != B[i][j]:
                return False
    return True


def add_matrix_365(A, B, counter):
    """Element-wise matrix addition. Counts one addition per element."""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
            counter.add(1)
    return C


def sub_matrix_365(A, B, counter):
    """Element-wise matrix subtraction. Counts one subtraction per element."""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
            counter.add(1)
    return C


def split_matrix_365(M):
    """Split matrix M into its four n/2 x n/2 quadrants."""
    n = len(M)
    mid = n // 2
    top_left = [row[:mid] for row in M[:mid]]
    top_right = [row[mid:] for row in M[:mid]]
    bottom_left = [row[:mid] for row in M[mid:]]
    bottom_right = [row[mid:] for row in M[mid:]]
    return top_left, top_right, bottom_left, bottom_right


def join_matrix_365(C11, C12, C21, C22):
    """Join four n/2 x n/2 quadrants back into one n x n matrix."""
    top = [r1 + r2 for r1, r2 in zip(C11, C12)]
    bottom = [r1 + r2 for r1, r2 in zip(C21, C22)]
    return top + bottom


# ---------------------------------------------------------------------
# 1(a) TRADITIONAL METHOD: triple nested loop, O(n^3)
# ---------------------------------------------------------------------
def multiply_traditional_365(A, B, counter):
    """Multiply two n x n matrices the classic way and count operations."""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]   # 1 multiplication + 1 addition
                counter.add(2)
            C[i][j] = total
    return C


# ---------------------------------------------------------------------
# 1(b) STRASSEN'S ALGORITHM: divide and conquer, 7 multiplications
# ---------------------------------------------------------------------
def multiply_strassen_365(A, B, counter, base_case=2):
    """
    Multiply two n x n matrices using Strassen's algorithm.
    base_case: below this size we switch to the traditional method,
    since recursion has no benefit for very small matrices.
    """
    n = len(A)

    if n <= base_case:
        return multiply_traditional_365(A, B, counter)

    A11, A12, A21, A22 = split_matrix_365(A)
    B11, B12, B21, B22 = split_matrix_365(B)

    # The 7 Strassen products (instead of the usual 8 for 4 quadrants)
    M1 = multiply_strassen_365(add_matrix_365(A11, A22, counter), add_matrix_365(B11, B22, counter), counter, base_case)
    M2 = multiply_strassen_365(add_matrix_365(A21, A22, counter), B11, counter, base_case)
    M3 = multiply_strassen_365(A11, sub_matrix_365(B12, B22, counter), counter, base_case)
    M4 = multiply_strassen_365(A22, sub_matrix_365(B21, B11, counter), counter, base_case)
    M5 = multiply_strassen_365(add_matrix_365(A11, A12, counter), B22, counter, base_case)
    M6 = multiply_strassen_365(sub_matrix_365(A21, A11, counter), add_matrix_365(B11, B12, counter), counter, base_case)
    M7 = multiply_strassen_365(sub_matrix_365(A12, A22, counter), add_matrix_365(B21, B22, counter), counter, base_case)

    C11 = add_matrix_365(sub_matrix_365(add_matrix_365(M1, M4, counter), M5, counter), M7, counter)
    C12 = add_matrix_365(M3, M5, counter)
    C21 = add_matrix_365(M2, M4, counter)
    C22 = add_matrix_365(sub_matrix_365(add_matrix_365(M1, M3, counter), M2, counter), M6, counter)

    return join_matrix_365(C11, C12, C21, C22)


# ---------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------
def main():
    print("=" * 70)
    print(" CSF302 Lab 3 - Q1: Matrix Multiplication (Traditional vs Strassen)")
    print(" Student No: 02240365")
    print("=" * 70)

    # ---- Part A: one small demo showing both resultant matrices ----
    n_demo365 = 4
    A = random_matrix_365(n_demo365)
    B = random_matrix_365(n_demo365)
    c1, c2 = StepCounter365(), StepCounter365()
    C_trad = multiply_traditional_365(A, B, c1)
    C_strassen = multiply_strassen_365(A, B, c2)

    print(f"\n--- Demo run for a {n_demo365}x{n_demo365} matrix ---")
    print_matrix_365(A, "Matrix A:")
    print_matrix_365(B, "Matrix B:")
    print_matrix_365(C_trad, "Result (Traditional):")
    print_matrix_365(C_strassen, "Result (Strassen):")
    print("Results match:", matrices_equal_365(C_trad, C_strassen))
    print(f"Traditional step count: {c1.count}")
    print(f"Strassen step count   : {c2.count}")

    # ---- Part B: step count & timing table across increasing sizes365 ----
    sizes365 = [2, 4, 8, 16, 32, 64, 128]
    trad_times365, strassen_times365 = [], []
    trad_steps365, strassen_steps365 = [], []

    print("\n--- Step/Frequency Count & Timing Table ---")
    header = f"{'n':>5} | {'Trad Steps':>12} | {'Strassen Steps':>15} | {'Trad Time(s)':>13} | {'Strassen Time(s)':>17} | Match"
    print(header)
    print("-" * len(header))

    for n in sizes365:
        A = random_matrix_365(n)
        B = random_matrix_365(n)

        c_trad, c_strassen = StepCounter365(), StepCounter365()

        start = time.perf_counter()
        C_trad = multiply_traditional_365(A, B, c_trad)
        t_trad = time.perf_counter() - start

        start = time.perf_counter()
        C_strassen = multiply_strassen_365(A, B, c_strassen)
        t_strassen = time.perf_counter() - start

        match = matrices_equal_365(C_trad, C_strassen)

        trad_times365.append(t_trad)
        strassen_times365.append(t_strassen)
        trad_steps365.append(c_trad.count)
        strassen_steps365.append(c_strassen.count)

        print(f"{n:>5} | {c_trad.count:>12} | {c_strassen.count:>15} | {t_trad:>13.6f} | {t_strassen:>17.6f} | {match}")

    # ---- Part C: plot the timing comparison graph ----
    plt.figure(figsize=(8, 5))
    plt.plot(sizes365, trad_times365, marker='o', label='Traditional O(n^3)')
    plt.plot(sizes365, strassen_times365, marker='s', label="Strassen O(n^2.81)")
    plt.xlabel('Matrix size (n)')
    plt.ylabel('Time taken (seconds)')
    plt.title('Matrix Multiplication: Traditional vs Strassen\n(Student No: 02240365)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('q1_time_complexity_graph.png', dpi=150)
    print("\nGraph saved as 'q1_time_complexity_graph.png'")

    # ---------------------------------------------------------------
    # CONCLUSION (as a comment / printed note, per deliverable 4)
    # ---------------------------------------------------------------
    # ANALYSIS / CONCLUSION:
    # The Traditional method performs n^3 multiplications, so its step
    # count grows cubically: T(n) = O(n^3). Strassen's algorithm replaces
    # one of the 8 quadrant multiplications with extra additions, giving
    # the recurrence T(n) = 7T(n/2) + O(n^2), which solves to O(n^2.81) -
    # fewer multiplications for large n. The step counts above confirm
    # this: Strassen's step count grows more slowly relative to n than
    # the Traditional method's as n increases. However, in this pure
    # Python implementation, Strassen is still slower in wall-clock time
    # up to n=128 because each split performs many extra O(n^2) matrix
    # additions/subtractions, and Python's per-operation overhead makes
    # this constant factor large. This matches theory: Strassen's lower
    # asymptotic complexity only pays off once n is large enough for the
    # multiplication savings to outweigh the addition overhead.
    print("\nCONCLUSION: Strassen's step count grows more slowly than the")
    print("Traditional method's as n increases, matching its better O(n^2.81)")
    print("complexity. Its wall-clock time is still higher here up to n=128")
    print("because of Python's overhead on the many extra matrix additions -")
    print("the crossover to a real speed advantage happens at larger n.")


if __name__ == "__main__":
    main()
