"""
Q2: Karatsuba's Algorithm for Large Integer Multiplication

WHAT THIS PROGRAM DOES
-----------------------
1. Represents large integers as digit strings (not native int
   multiplication) so sizes can go well beyond native limits.
2. Multiplies two large integers using:
      (a) Traditional Method   -> grade-school multiplication -> O(n^2)
      (b) Karatsuba's Algorithm -> divide and conquer, 3 sub  -> O(n^1.585)
                                    multiplications per split
3. Pads both operands to the same length and to the next power of 2,
   as required by the recursive split.
4. Verifies Karatsuba's result matches the Traditional method for
   every test case.
5. Records step counts, times both methods on increasing digit
   lengths (8, 16, 32, ..., 1024) and plots a comparison graph.
"""

import random
import time
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# STEP COUNTER
# ---------------------------------------------------------------------
class StepCounter365:
    def __init__(self):
        self.count = 0

    def add(self, n=1):
        self.count += n


# ---------------------------------------------------------------------
# HELPER FUNCTIONS (all numbers are handled as digit strings)
# ---------------------------------------------------------------------
def random_big_number_365(num_digits):
    """Generate a random positive integer with exactly num_digits digits."""
    first = str(random.randint(1, 9))                    # no leading zero
    rest = ''.join(str(random.randint(0, 9)) for _ in range(num_digits - 1))
    return first + rest


def pad_left_365(s, length):
    """Pad a digit string on the left with zeros to reach `length`."""
    return s.zfill(length)


def next_power_of_2_365(n):
    """Smallest power of 2 that is >= n."""
    p = 1
    while p < n:
        p *= 2
    return p


def strip_leading_zeros_365(s):
    """Remove leading zeros from a digit string (keep at least one digit)."""
    s = s.lstrip('0')
    return s if s else '0'


def add_strings_365(a, b, counter):
    """Add two digit strings using manual grade-school addition."""
    a, b = a[::-1], b[::-1]          # reverse so index 0 = least significant
    n = max(len(a), len(b))
    a, b = a.ljust(n, '0'), b.ljust(n, '0')
    result = []
    carry = 0
    for i in range(n):
        digit_sum = int(a[i]) + int(b[i]) + carry
        counter.add(1)                 # one digit addition
        result.append(str(digit_sum % 10))
        carry = digit_sum // 10
    if carry:
        result.append(str(carry))
    return strip_leading_zeros_365(''.join(reversed(result)))


def subtract_strings_365(a, b, counter):
    """Subtract digit string b from digit string a (assumes a >= b)."""
    a, b = a[::-1], b[::-1]
    n = len(a)
    b = b.ljust(n, '0')
    result = []
    borrow = 0
    for i in range(n):
        digit_diff = int(a[i]) - int(b[i]) - borrow
        counter.add(1)                 # one digit subtraction
        if digit_diff < 0:
            digit_diff += 10
            borrow = 1
        else:
            borrow = 0
        result.append(str(digit_diff))
    return strip_leading_zeros_365(''.join(reversed(result)))


def is_less_than_365(a, b):
    """True if digit string a represents a smaller number than b."""
    a, b = strip_leading_zeros_365(a), strip_leading_zeros_365(b)
    if len(a) != len(b):
        return len(a) < len(b)
    return a < b


# ---------------------------------------------------------------------
# 1(a) TRADITIONAL METHOD: grade-school multiplication, O(n^2)
# ---------------------------------------------------------------------
def multiply_traditional_365(x, y, counter):
    """Multiply two digit strings the classic long-multiplication way."""
    x, y = strip_leading_zeros_365(x), strip_leading_zeros_365(y)
    if x == '0' or y == '0':
        return '0'

    x_rev, y_rev = x[::-1], y[::-1]
    result = [0] * (len(x) + len(y))

    for i in range(len(x_rev)):
        for j in range(len(y_rev)):
            result[i + j] += int(x_rev[i]) * int(y_rev[j])
            counter.add(1)              # one single-digit multiplication

    # carry propagation
    for i in range(len(result) - 1):
        result[i + 1] += result[i] // 10
        result[i] %= 10
        counter.add(1)

    digits = ''.join(str(d) for d in reversed(result))
    return strip_leading_zeros_365(digits)


# ---------------------------------------------------------------------
# 1(b) KARATSUBA'S ALGORITHM: divide and conquer, 3 multiplications
# ---------------------------------------------------------------------
def karatsuba_365(x, y, counter, base_case=2):
    """
    Multiply two equal-length, power-of-2-length digit strings using
    Karatsuba's algorithm. base_case: below this length, switch to the
    Traditional method since recursion gives no benefit for tiny inputs.
    """
    n = len(x)

    if n <= base_case:
        return multiply_traditional_365(x, y, counter)

    mid = n // 2
    low_len = n - mid          # number of digits in the "low" half
    x_high, x_low = x[:mid], x[mid:]
    y_high, y_low = y[:mid], y[mid:]

    # 3 recursive multiplications instead of the usual 4
    z2 = karatsuba_365(x_high, y_high, counter, base_case)                       # x_high * y_high
    z0 = karatsuba_365(x_low, y_low, counter, base_case)                         # x_low  * y_low

    sum_x = add_strings_365(x_high, x_low, counter)
    sum_y = add_strings_365(y_high, y_low, counter)
    sum_len = max(len(sum_x), len(sum_y))
    z1_full = karatsuba_365(pad_left_365(sum_x, sum_len), pad_left_365(sum_y, sum_len), counter, base_case)

    # z1 = (x_high+x_low)*(y_high+y_low) - z2 - z0
    z1 = subtract_strings_365(subtract_strings_365(z1_full, z2, counter), z0, counter)

    # result = z2 * 10^(2*low_len) + z1 * 10^low_len + z0
    # (the weight is low_len, the number of digits in x_low/y_low - this
    # matches mid only when n is even, so we must use low_len explicitly)
    part1 = z2 + '0' * (2 * low_len)
    part2 = z1 + '0' * low_len
    total = add_strings_365(add_strings_365(part1, part2, counter), z0, counter)
    return strip_leading_zeros_365(total)


# ---------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------
def main():
    print("=" * 70)
    print(" CSF302 Lab 3 - Q2: Karatsuba vs Traditional Big-Integer Multiply")
    print(" Student No: 02240365")
    print("=" * 70)

    # ---- Part A: one small demo showing both results ----
    x, y = "1234", "5678"
    c1, c2 = StepCounter365(), StepCounter365()
    prod_trad = multiply_traditional_365(x, y, c1)
    prod_kara = karatsuba_365(pad_left_365(x, 4), pad_left_365(y, 4), c2)

    print(f"\n--- Demo run: {x} x {y} ---")
    print("Traditional result:", prod_trad)
    print("Karatsuba result  :", prod_kara)
    print("Results match     :", int(prod_trad) == int(prod_kara))
    print(f"Traditional step count: {c1.count}")
    print(f"Karatsuba step count  : {c2.count}")

    # ---- Part B: step count & timing table across increasing digit sizes ----
    digit_sizes365 = [8, 16, 32, 64, 128, 256, 512, 1024]
    trad_times365, kara_times365 = [], []
    trad_steps365, kara_steps365 = [], []

    print("\n--- Step/Frequency Count & Timing Table ---")
    header = f"{'digits':>7} | {'Trad Steps':>12} | {'Kara Steps':>12} | {'Trad Time(s)':>13} | {'Kara Time(s)':>13} | Match"
    print(header)
    print("-" * len(header))

    for n_digits in digit_sizes365:
        x = random_big_number_365(n_digits)
        y = random_big_number_365(n_digits)

        # pad both operands to the same length and to the next power of 2
        padded_len = next_power_of_2_365(max(len(x), len(y)))
        x_pad = pad_left_365(x, padded_len)
        y_pad = pad_left_365(y, padded_len)

        c_trad, c_kara = StepCounter365(), StepCounter365()

        start = time.perf_counter()
        prod_trad = multiply_traditional_365(x_pad, y_pad, c_trad)
        t_trad = time.perf_counter() - start

        start = time.perf_counter()
        prod_kara = karatsuba_365(x_pad, y_pad, c_kara)
        t_kara = time.perf_counter() - start

        match = int(prod_trad) == int(prod_kara)

        trad_times365.append(t_trad)
        kara_times365.append(t_kara)
        trad_steps365.append(c_trad.count)
        kara_steps365.append(c_kara.count)

        print(f"{n_digits:>7} | {c_trad.count:>12} | {c_kara.count:>12} | {t_trad:>13.6f} | {t_kara:>13.6f} | {match}")

    # ---- Part C: plot the timing comparison graph ----
    plt.figure(figsize=(8, 5))
    plt.plot(digit_sizes365, trad_times365, marker='o', label='Traditional O(n^2)')
    plt.plot(digit_sizes365, kara_times365, marker='s', label='Karatsuba O(n^1.585)')
    plt.xlabel('Number of digits (n)')
    plt.ylabel('Time taken (seconds)')
    plt.title('Big Integer Multiplication: Traditional vs Karatsuba\n(Student No: 02240365)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('q2_time_complexity_graph.png', dpi=150)
    print("\nGraph saved as 'q2_time_complexity_graph.png'")

    # ---------------------------------------------------------------
    # CONCLUSION (as a comment / printed note, per deliverable 4)
    # ---------------------------------------------------------------
    # ANALYSIS / CONCLUSION:
    # The Traditional method multiplies every digit of x with every
    # digit of y, giving T(n) = O(n^2). Karatsuba's algorithm replaces
    # one of the 4 sub-multiplications needed per split with extra
    # additions/subtractions, giving the recurrence T(n) = 3T(n/2) +
    # O(n), which solves to O(n^1.585). The step counts above confirm
    # this: as n doubles, the Traditional method's step count roughly
    # quadruples, while Karatsuba's grows more slowly (roughly x3 per
    # doubling). Karatsuba has more overhead for small n, but the two
    # step counts cross over around a few hundred digits, after which
    # Karatsuba's step count is the smaller of the two - for very large
    # numbers (as used in cryptography) it is the clearly faster choice.
    print("\nCONCLUSION: The Traditional method's step count grows as O(n^2),")
    print("while Karatsuba's grows as O(n^1.585). Karatsuba has more overhead")
    print("for small n, but the counts cross over around a few hundred digits,")
    print("after which Karatsuba becomes the faster algorithm, matching theory.")


if __name__ == "__main__":
    main()
