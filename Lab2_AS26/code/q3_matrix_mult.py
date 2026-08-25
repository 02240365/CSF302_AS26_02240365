"""
CSF302 - Lab 2
Q3: Square Matrix Multiplication

WHAT THIS PROGRAM DOES
-----------------------
1. Lets the user manually enter two n x n matrices OR randomly generate
   them, where n MUST be a power of 2 (2, 4, 8, 16, ...).
2. Multiplies the two matrices using the standard (naive) O(n^3)
   algorithm and displays the resultant matrix.
3. Counts the number of basic operations (multiplications + additions)
   performed - the step/frequency count.
4. Also runs Strassen's Algorithm (the well-known divide-and-conquer
   matrix multiplication algorithm, O(n^2.81)) on the SAME matrices,
   counts ITS basic operations, and compares the two step counts
   directly. This is the file `q3_strassen.py` referenced in the
   deliverables list, imported here for the side-by-side comparison.
"""

import random
import time
import matplotlib.pyplot as plt

from q3_strassen import strassen_multiply_365, next_power_of_2_365


# ---------------------------------------------------------------------
# Helpers: build / display / generate matrices
# ---------------------------------------------------------------------
def is_power_of_2_365(n365):
    return n365 > 0 and (n365 & (n365 - 1)) == 0


def generate_matrix_365(n365, low365=0, high365=9):
    return [[random.randint(low365, high365) for _ in range(n365)] for _ in range(n365)]


def input_matrix_manually_365(n365, name365):
    print(f"Enter matrix {name365} row by row ({n365} values per row, space separated):")
    matrix365 = []
    for row_idx365 in range(n365):
        row365 = list(map(int, input(f"Row {row_idx365 + 1}: ").split()))
        while len(row365) != n365:
            print(f"Row must have exactly {n365} numbers, try again.")
            row365 = list(map(int, input(f"Row {row_idx365 + 1}: ").split()))
        matrix365.append(row365)
    return matrix365


def display_matrix_365(matrix365, name365="Matrix"):
    print(f"\n{name365}:")
    for row365 in matrix365:
        print(row365)


# ---------------------------------------------------------------------
# NAIVE SQUARE MATRIX MULTIPLICATION with step/frequency counting
# ---------------------------------------------------------------------
def multiply_matrices_naive_365(a365, b365):
    """
    Standard triple-nested-loop matrix multiplication: O(n^3).
    Returns (result_matrix, step_count) where step_count counts every
    scalar multiplication AND every scalar addition performed.
    """
    n365 = len(a365)
    result365 = [[0] * n365 for _ in range(n365)]
    steps365 = 0

    for i365 in range(n365):
        for j365 in range(n365):
            total365 = 0
            for k365 in range(n365):
                total365 += a365[i365][k365] * b365[k365][j365]
                steps365 += 2                 # 1 multiplication + 1 addition
            result365[i365][j365] = total365

    return result365, steps365


# ---------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------
def main():
    print("=" * 70)
    print(" CSF302 Lab 2 - Q3: SQUARE MATRIX MULTIPLICATION (Student No: 02240365)")
    print("=" * 70)

    n365 = int(input("Enter matrix size n (must be a power of 2, e.g. 2,4,8,16): "))
    while not is_power_of_2_365(n365):
        print("n must be a power of 2 (2, 4, 8, 16, ...). Try again.")
        n365 = int(input("Enter matrix size n: "))

    mode365 = input("Type 'M' for manual input or 'R' for random generation: ").strip().upper()

    if mode365 == "M":
        matrix_a365 = input_matrix_manually_365(n365, "A")
        matrix_b365 = input_matrix_manually_365(n365, "B")
    else:
        matrix_a365 = generate_matrix_365(n365)
        matrix_b365 = generate_matrix_365(n365)

    display_matrix_365(matrix_a365, "Matrix A")
    display_matrix_365(matrix_b365, "Matrix B")

    # ---------------- Naive multiplication ----------------
    start365 = time.perf_counter()
    result_naive365, steps_naive365 = multiply_matrices_naive_365(matrix_a365, matrix_b365)
    time_naive365 = time.perf_counter() - start365

    display_matrix_365(result_naive365, "Result (Naive Multiplication)")
    print(f"\nNaive multiplication step/frequency count : {steps_naive365}")
    print(f"Naive multiplication time                 : {time_naive365:.6f} seconds")

    # ---------------- OPTIONAL: Strassen's algorithm ----------------
    start365 = time.perf_counter()
    result_strassen365, steps_strassen365 = strassen_multiply_365(matrix_a365, matrix_b365)
    time_strassen365 = time.perf_counter() - start365

    display_matrix_365(result_strassen365, "Result (Strassen's Algorithm)")
    print(f"\nStrassen's algorithm step/frequency count : {steps_strassen365}")
    print(f"Strassen's algorithm time                 : {time_strassen365:.6f} seconds")

    same_result365 = result_naive365 == result_strassen365
    print(f"\nBoth methods produce the same result matrix: {same_result365}")

    # ---------------- Graph: step count comparison across sizes ----------------
    sizes365 = [2, 4, 8, 16, 32, 64]
    naive_steps365 = []
    strassen_steps365 = []

    for size365 in sizes365:
        a_test365 = generate_matrix_365(size365)
        b_test365 = generate_matrix_365(size365)

        _, s_naive365 = multiply_matrices_naive_365(a_test365, b_test365)
        _, s_strassen365 = strassen_multiply_365(a_test365, b_test365)

        naive_steps365.append(s_naive365)
        strassen_steps365.append(s_strassen365)

    plt.figure(figsize=(8, 5))
    plt.plot(sizes365, naive_steps365, marker='o', label='Naive O(n^3)')
    plt.plot(sizes365, strassen_steps365, marker='s', label="Strassen O(n^2.81)")
    plt.xlabel('Matrix size (n x n)')
    plt.ylabel('Step / Basic Operation Count')
    plt.title('Matrix Multiplication: Naive vs Strassen - Step Count Comparison\n(Student No: 02240365)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('q3_matrix_step_count_graph.png', dpi=150)
    print("\nGraph saved as 'q3_matrix_step_count_graph.png'")

    # ------------------------------------------------------------
    # ANALYSIS / CONCLUSION:
    # The naive triple-loop method performs O(n^3) basic operations,
    # so its step count grows very quickly as matrix size n doubles
    # (each doubling multiplies the step count by roughly 8x).
    # Strassen's divide-and-conquer algorithm reduces the number of
    # recursive multiplications from 8 to 7 per split, giving it a
    # better asymptotic complexity of O(n^2.81). For small matrices the
    # overhead of Strassen's extra additions/subtractions can make it
    # comparable to or slower than the naive method, but as n grows
    # large, Strassen's step count grows more slowly, making it the
    # more efficient algorithm for large matrices.
    # ------------------------------------------------------------
    print("\nCONCLUSION: For large n, Strassen's algorithm performs fewer")
    print("basic operations than the naive O(n^3) method, though the naive")
    print("method can be simpler and competitive for small matrices.")


if __name__ == "__main__":
    main()
