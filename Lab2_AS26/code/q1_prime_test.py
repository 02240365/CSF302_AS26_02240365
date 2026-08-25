"""
CSF302 - Lab 2
Q1: Prime Number Testing

WHAT THIS PROGRAM DOES
-----------------------
1. Takes at least 10 numbers from the user.
2. Checks whether each number is prime using:
      (a) Naive Method       -> checks divisors from 2 to n-1        -> O(n)
      (b) Optimized Method   -> checks divisors from 2 to sqrt(n)    -> O(sqrt(n))
3. Counts the number of "basic operations" (step/frequency count) each
   method performs for every input number, and prints a comparison table.
4. OPTIONAL: Generates all prime numbers up to a limit using the
   Sieve of Eratosthenes and reports its own step count.
5. Plots a graph (time vs input size) comparing Naive vs Optimized so the
   faster algorithm can be identified visually.
"""

import random
import time
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# 1(a) NAIVE METHOD: check divisibility from 2 to n-1
# ---------------------------------------------------------------------
def is_prime_naive_365(n365):
    """Return (is_prime, step_count) using the naive O(n) method."""
    steps365 = 0                      # counts every basic comparison made

    if n365 < 2:                      # 0 and 1 (and negatives) are not prime
        return False, steps365

    for i365 in range(2, n365):       # check every number from 2 to n-1
        steps365 += 1                 # one "step" = one division/modulus check
        if n365 % i365 == 0:
            return False, steps365    # found a divisor -> not prime

    return True, steps365


# ---------------------------------------------------------------------
# 1(b) OPTIMIZED METHOD: check divisibility up to sqrt(n) only
# ---------------------------------------------------------------------
def is_prime_optimized_365(n365):
    """Return (is_prime, step_count) using the optimized O(sqrt(n)) method."""
    steps365 = 0

    if n365 < 2:
        return False, steps365
    if n365 in (2, 3):
        return True, steps365

    steps365 += 1                     # step for the "n % 2 == 0" check below
    if n365 % 2 == 0:
        return False, steps365

    i365 = 3
    while i365 * i365 <= n365:        # only loop up to sqrt(n)
        steps365 += 1
        if n365 % i365 == 0:
            return False, steps365
        i365 += 2                     # skip even numbers -> fewer checks

    return True, steps365


# ---------------------------------------------------------------------
# 1(c) OPTIONAL: SIEVE OF ERATOSTHENES -> list every prime up to a limit
# ---------------------------------------------------------------------
def sieve_of_eratosthenes_365(limit365):
    """Return (list_of_primes, step_count) for all primes <= limit365."""
    steps365 = 0
    is_prime_list365 = [True] * (limit365 + 1)
    is_prime_list365[0:2] = [False, False]   # 0 and 1 are not prime

    p365 = 2
    while p365 * p365 <= limit365:
        steps365 += 1
        if is_prime_list365[p365]:
            for multiple365 in range(p365 * p365, limit365 + 1, p365):
                steps365 += 1                 # one step per number marked off
                is_prime_list365[multiple365] = False
        p365 += 1

    primes365 = [num365 for num365, flag365 in enumerate(is_prime_list365) if flag365]
    return primes365, steps365


# ---------------------------------------------------------------------
# Helper: get at least 10 numbers from the user
# ---------------------------------------------------------------------
def get_input_numbers_365():
    print("Enter at least 10 numbers to test (space-separated),")
    print("or press ENTER to auto-generate 10 random numbers:")
    raw365 = input(">> ").strip()

    if raw365 == "":
        numbers365 = [random.randint(2, 100000) for _ in range(10)]
        print(f"Auto-generated numbers: {numbers365}")
        return numbers365

    numbers365 = [int(x365) for x365 in raw365.split()]
    while len(numbers365) < 10:
        print(f"You entered only {len(numbers365)} numbers. Need at least 10.")
        extra365 = input("Enter more numbers: ").strip().split()
        numbers365 += [int(x365) for x365 in extra365]

    return numbers365


# ---------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------
def main():
    print("=" * 70)
    print(" CSF302 Lab 2 - Q1: PRIME NUMBER TESTING (Student No: 02240365)")
    print("=" * 70)

    numbers365 = get_input_numbers_365()

    # table header
    print("\n{:<12}{:<10}{:<10}{:<15}{:<15}".format(
        "Number", "Naive?", "Optim?", "NaiveSteps", "OptimSteps"))
    print("-" * 62)

    naive_steps_list365 = []
    optim_steps_list365 = []

    for n365 in numbers365:
        is_p_naive365, steps_naive365 = is_prime_naive_365(n365)
        is_p_opt365, steps_opt365 = is_prime_optimized_365(n365)

        naive_steps_list365.append(steps_naive365)
        optim_steps_list365.append(steps_opt365)

        print("{:<12}{:<10}{:<10}{:<15}{:<15}".format(
            n365, str(is_p_naive365), str(is_p_opt365),
            steps_naive365, steps_opt365))

    # ------------------------------------------------------------
    # OPTIONAL PART: Sieve of Eratosthenes
    # ------------------------------------------------------------
    sieve_limit365 = max(numbers365)
    primes365, sieve_steps365 = sieve_of_eratosthenes_365(sieve_limit365)
    print("\n--- OPTIONAL: Sieve of Eratosthenes up to", sieve_limit365, "---")
    print(f"Number of primes found: {len(primes365)}")
    print(f"Sieve step count      : {sieve_steps365}")
    print(f"First 20 primes found : {primes365[:20]}")

    # ------------------------------------------------------------
    # TIME COMPLEXITY COMPARISON GRAPH
    # We time both algorithms on increasing input sizes (n) to
    # visually show which one grows faster.
    # ------------------------------------------------------------
    test_sizes365 = [1000, 5000, 10000, 50000, 100000, 300000, 600000, 1000000]
    naive_times365 = []
    optim_times365 = []
    repeats365 = 50          # repeat & average to smooth out timing noise

    for size365 in test_sizes365:
        # find an actual PRIME near `size` -> this is the worst case for
        # both algorithms (no early exit possible), giving a fair timing
        # comparison that clearly reflects each algorithm's growth rate
        test_n365 = size365 + 1
        while not is_prime_optimized_365(test_n365)[0]:
            test_n365 += 1

        start365 = time.perf_counter()
        for _ in range(repeats365):
            is_prime_naive_365(test_n365)
        naive_times365.append((time.perf_counter() - start365) / repeats365)

        start365 = time.perf_counter()
        for _ in range(repeats365):
            is_prime_optimized_365(test_n365)
        optim_times365.append((time.perf_counter() - start365) / repeats365)

    plt.figure(figsize=(8, 5))
    plt.plot(test_sizes365, naive_times365, marker='o', label='Naive O(n)')
    plt.plot(test_sizes365, optim_times365, marker='s', label='Optimized O(sqrt n)')
    plt.xlabel('Input number (n)')
    plt.ylabel('Time taken (seconds)')
    plt.title('Prime Testing: Naive vs Optimized - Time Complexity Comparison\n(Student No: 02240365)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('q1_time_complexity_graph.png', dpi=150)
    print("\nGraph saved as 'q1_time_complexity_graph.png'")

    # ------------------------------------------------------------
    # CONCLUSION (as a comment / printed note, per deliverable 4)
    # ------------------------------------------------------------
    # ANALYSIS / CONCLUSION:
    # The Naive method checks up to (n-1) divisors, giving it O(n) time
    # complexity, so its step count and run time grow linearly with n.
    # The Optimized method only checks divisors up to sqrt(n), giving it
    # O(sqrt(n)) time complexity - its step count and run time grow far
    # more slowly as n increases. The graph clearly shows the Optimized
    # method's curve staying near-flat while the Naive method's curve
    # rises steeply for large inputs, confirming the Optimized method
    # is the faster algorithm, especially for large prime numbers
    # (the worst case for both methods).
    print("\nCONCLUSION: The Optimized (sqrt-n) method is faster than the")
    print("Naive method, especially as the input number n grows large.")


if __name__ == "__main__":
    main()
