"""
CSF302 - Lab 2
Q3 (OPTIONAL EXTENSION): Strassen's Matrix Multiplication Algorithm
Student No: 02240365  (variables use last 3 digits -> 365)

Strassen's algorithm multiplies two n x n matrices using only 7
recursive multiplications (instead of the 8 that the naive
divide-and-conquer approach would need), giving it a better
asymptotic time complexity of O(n^2.81) compared to the naive
method's O(n^3).

This file is imported by q3_matrix_mult.py so both algorithms can be
compared on the exact same input matrices, and can also be run
directly for a quick standalone demo.
"""

import random


def next_power_of_2_365(n365):
    """Return the smallest power of 2 that is >= n365."""
    power365 = 1
    while power365 < n365:
        power365 *= 2
    return power365


# ---------------------------------------------------------------------
# Basic matrix helpers (add / subtract / split / combine)
# ---------------------------------------------------------------------
def add_matrix_365(a365, b365):
    n365 = len(a365)
    return [[a365[i365][j365] + b365[i365][j365] for j365 in range(n365)] for i365 in range(n365)]


def subtract_matrix_365(a365, b365):
    n365 = len(a365)
    return [[a365[i365][j365] - b365[i365][j365] for j365 in range(n365)] for i365 in range(n365)]


def split_matrix_365(m365):
    """Split matrix m365 into 4 equal quadrants: top-left, top-right, bottom-left, bottom-right."""
    n365 = len(m365)
    mid365 = n365 // 2

    top_left365 = [row365[:mid365] for row365 in m365[:mid365]]
    top_right365 = [row365[mid365:] for row365 in m365[:mid365]]
    bottom_left365 = [row365[:mid365] for row365 in m365[mid365:]]
    bottom_right365 = [row365[mid365:] for row365 in m365[mid365:]]

    return top_left365, top_right365, bottom_left365, bottom_right365


def combine_quadrants_365(c11365, c12365, c21365, c22365):
    """Combine 4 quadrants back into a single matrix."""
    top365 = [r1365 + r2365 for r1365, r2365 in zip(c11365, c12365)]
    bottom365 = [r1365 + r2365 for r1365, r2365 in zip(c21365, c22365)]
    return top365 + bottom365


# ---------------------------------------------------------------------
# STRASSEN'S ALGORITHM with step/frequency counting
# ---------------------------------------------------------------------
def strassen_365(a365, b365, steps_holder365):
    """
    Recursively multiply a365 x b365 using Strassen's algorithm.
    steps_holder365 is a single-element list used as a mutable counter
    so every recursive call can add to the same running total.
    """
    n365 = len(a365)

    # Base case: 1x1 "matrix" multiplication is just one scalar multiply
    if n365 == 1:
        steps_holder365[0] += 1
        return [[a365[0][0] * b365[0][0]]]

    a11365, a12365, a21365, a22365 = split_matrix_365(a365)
    b11365, b12365, b21365, b22365 = split_matrix_365(b365)

    # 7 recursive multiplications (Strassen's key trick: 7 instead of 8)
    m1365 = strassen_365(add_matrix_365(a11365, a22365), add_matrix_365(b11365, b22365), steps_holder365)
    m2365 = strassen_365(add_matrix_365(a21365, a22365), b11365, steps_holder365)
    m3365 = strassen_365(a11365, subtract_matrix_365(b12365, b22365), steps_holder365)
    m4365 = strassen_365(a22365, subtract_matrix_365(b21365, b11365), steps_holder365)
    m5365 = strassen_365(add_matrix_365(a11365, a12365), b22365, steps_holder365)
    m6365 = strassen_365(subtract_matrix_365(a21365, a11365), add_matrix_365(b11365, b12365), steps_holder365)
    m7365 = strassen_365(subtract_matrix_365(a12365, a22365), add_matrix_365(b21365, b22365), steps_holder365)

    # combine the 7 products into the 4 result quadrants (each +/- is a step)
    c11365 = add_matrix_365(subtract_matrix_365(add_matrix_365(m1365, m4365), m5365), m7365)
    c12365 = add_matrix_365(m3365, m5365)
    c21365 = add_matrix_365(m2365, m4365)
    c22365 = add_matrix_365(subtract_matrix_365(add_matrix_365(m1365, m3365), m2365), m6365)
    steps_holder365[0] += 18   # 18 scalar +/- operations used to combine quadrants

    return combine_quadrants_365(c11365, c12365, c21365, c22365)


def strassen_multiply_365(a365, b365):
    """
    Public entry point. Pads matrices up to the next power of 2 if
    needed, runs Strassen's algorithm, then trims the result back
    down to the original size. Returns (result_matrix, step_count).
    """
    original_n365 = len(a365)
    padded_n365 = next_power_of_2_365(original_n365)

    if padded_n365 != original_n365:
        a_padded365 = [row365 + [0] * (padded_n365 - original_n365) for row365 in a365]
        a_padded365 += [[0] * padded_n365 for _ in range(padded_n365 - original_n365)]
        b_padded365 = [row365 + [0] * (padded_n365 - original_n365) for row365 in b365]
        b_padded365 += [[0] * padded_n365 for _ in range(padded_n365 - original_n365)]
    else:
        a_padded365, b_padded365 = a365, b365

    steps_holder365 = [0]
    result_padded365 = strassen_365(a_padded365, b_padded365, steps_holder365)

    # trim back to original size
    result365 = [row365[:original_n365] for row365 in result_padded365[:original_n365]]
    return result365, steps_holder365[0]


# ---------------------------------------------------------------------
# Quick standalone demo (only runs if this file is executed directly)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    n365 = 4
    a365 = [[random.randint(0, 9) for _ in range(n365)] for _ in range(n365)]
    b365 = [[random.randint(0, 9) for _ in range(n365)] for _ in range(n365)]

    print("Matrix A:", a365)
    print("Matrix B:", b365)

    result365, steps365 = strassen_multiply_365(a365, b365)
    print("Result (Strassen):", result365)
    print("Step/frequency count:", steps365)
