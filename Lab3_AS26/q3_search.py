"""
CSF302 - Lab 3
Q3: Binary Search vs Ternary Search (Menu-Driven Program)

WHAT THIS PROGRAM DOES
-----------------------
A menu-driven program that:
 1. Generates n sorted random numbers into an array
 2. Displays the array
 3. Searches for a key using Binary Search
 4. Searches for a key using Ternary Search
 5. Shows step/frequency count for the BEST case (key present,
    minimum comparisons - the middle element)
 6. Shows step/frequency count for the WORST case (key absent /
    last comparison needed)
 7. Shows a step/frequency count comparison table for both searches
    across increasing n
 0. Exit

Both search functions return (found_index, steps) so every search
records how many comparisons it made (step/frequency count).

Student No: 02240365
"""

import random
import time
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# 3/4(a) BINARY SEARCH: divide the range into 2 parts, O(log2 n)
# ---------------------------------------------------------------------
def binary_search_365(arr365, key365):
    """Search for key365 in sorted arr365. Returns (index or -1, steps)."""
    low365 = 0
    high365 = len(arr365) - 1
    steps365 = 0

    while low365 <= high365:
        mid365 = (low365 + high365) // 2
        steps365 += 1                       # one comparison step
        if arr365[mid365] == key365:
            return mid365, steps365
        elif arr365[mid365] < key365:
            low365 = mid365 + 1
        else:
            high365 = mid365 - 1

    return -1, steps365


# ---------------------------------------------------------------------
# 3/4(b) TERNARY SEARCH: divide the range into 3 parts, O(log3 n)
# ---------------------------------------------------------------------
def ternary_search_365(arr365, key365):
    """Search for key365 in sorted arr365. Returns (index or -1, steps)."""
    low365 = 0
    high365 = len(arr365) - 1
    steps365 = 0

    while low365 <= high365:
        third365 = (high365 - low365) // 3
        mid1_365 = low365 + third365
        mid2_365 = high365 - third365

        steps365 += 1                       # comparison at mid1
        if arr365[mid1_365] == key365:
            return mid1_365, steps365

        steps365 += 1                       # comparison at mid2
        if arr365[mid2_365] == key365:
            return mid2_365, steps365

        if key365 < arr365[mid1_365]:
            high365 = mid1_365 - 1
        elif key365 > arr365[mid2_365]:
            low365 = mid2_365 + 1
        else:
            low365 = mid1_365 + 1
            high365 = mid2_365 - 1

    return -1, steps365


# ---------------------------------------------------------------------
# MENU ACTIONS
# ---------------------------------------------------------------------
def generate_array_365(n365):
    """Generate n365 sorted random numbers (duplicates removed so every
    search key is unique, which keeps best/worst case counts meaningful)."""
    numbers365 = random.sample(range(1, n365 * 10 + 1), n365)
    return sorted(numbers365)


def display_array_365(arr365):
    if arr365 is None:
        print("No array generated yet. Choose option 1 first.")
        return
    print(f"Array (size {len(arr365)}):")
    print(arr365 if len(arr365) <= 30 else str(arr365[:30]) + " ... (truncated)")


def best_case_365(arr365):
    """Best case: search for the middle element - Binary Search finds it
    in exactly 1 step; Ternary Search usually finds it in 1-2 steps."""
    if arr365 is None:
        print("Generate an array first (option 1).")
        return
    mid_value365 = arr365[len(arr365) // 2]
    _, steps_bin365 = binary_search_365(arr365, mid_value365)
    _, steps_ter365 = ternary_search_365(arr365, mid_value365)
    print(f"\nBest case key (middle element) = {mid_value365}")
    print(f"Binary Search  steps: {steps_bin365}")
    print(f"Ternary Search steps: {steps_ter365}")


def worst_case_365(arr365):
    """Worst case: search for a key that is NOT in the array, so both
    algorithms must narrow the range all the way down before giving up."""
    if arr365 is None:
        print("Generate an array first (option 1).")
        return
    missing_key365 = arr365[-1] + 1          # guaranteed not present
    _, steps_bin365 = binary_search_365(arr365, missing_key365)
    _, steps_ter365 = ternary_search_365(arr365, missing_key365)
    print(f"\nWorst case key (not in array) = {missing_key365}")
    print(f"Binary Search  steps: {steps_bin365}")
    print(f"Ternary Search steps: {steps_ter365}")


def comparison_table_365():
    """
    Build a sorted array for several increasing sizes of n, search for
    a worst-case (missing) key in each with both algorithms, print a
    step-count table, and plot a comparison graph.
    """
    sizes365 = [100, 1000, 10000, 100000, 1000000]
    bin_steps365, ter_steps365 = [], []

    print("\n--- Step/Frequency Count Comparison Table (worst case) ---")
    print(f"{'n':>10}{'Binary Steps':>15}{'Ternary Steps':>16}")
    print("-" * 41)

    for n365 in sizes365:
        arr365 = list(range(1, n365 + 1))    # already sorted, no duplicates
        missing_key365 = n365 + 1            # worst case: key not present

        _, s_bin365 = binary_search_365(arr365, missing_key365)
        _, s_ter365 = ternary_search_365(arr365, missing_key365)

        bin_steps365.append(s_bin365)
        ter_steps365.append(s_ter365)
        print(f"{n365:>10}{s_bin365:>15}{s_ter365:>16}")

    # plot the comparison graph
    plt.figure(figsize=(8, 5))
    plt.plot(sizes365, bin_steps365, marker='o', label='Binary Search O(log2 n)')
    plt.plot(sizes365, ter_steps365, marker='s', label='Ternary Search O(log3 n)')
    plt.xscale('log')
    plt.xlabel('Array size (n)')
    plt.ylabel('Number of comparisons (steps)')
    plt.title('Binary vs Ternary Search: Step Count Comparison\n(Student No: 02240365)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('q3_time_complexity_graph.png', dpi=150)
    print("\nGraph saved as 'q3_time_complexity_graph.png'")

    # -----------------------------------------------------------
    # ANALYSIS / CONCLUSION:
    # Binary Search halves the search range every step, so its
    # recurrence is T(n) = T(n/2) + O(1), which solves to O(log2 n).
    # Ternary Search splits the range into 3 parts every step, so its
    # recurrence is T(n) = T(n/3) + O(1), which solves to O(log3 n).
    # Although log3(n) is a smaller number of ROUNDS than log2(n),
    # each Ternary Search round does 2 comparisons instead of 1, so
    # its total comparison count is about (2 * log3 n) versus Binary
    # Search's (log2 n). Since 2*log3(n) = 2*log2(n)/log2(3) is about
    # 1.26 * log2(n), Binary Search performs fewer comparisons overall
    # for the same n, which is exactly what the table above shows.
    print("\nCONCLUSION: Binary Search needs fewer total comparisons than")
    print("Ternary Search for the same n. Ternary Search needs fewer ROUNDS")
    print("(log3 n vs log2 n) but does 2 comparisons per round instead of 1,")
    print("so its total step count (about 1.26 x log2 n) is still higher.")


# ---------------------------------------------------------------------
# MAIN MENU LOOP
# ---------------------------------------------------------------------
def main():
    current_array_365 = None

    menu365 = """
========================================================================
 CSF302 Lab 3 - Q3: Binary Search vs Ternary Search (Student No: 02240365)
========================================================================
 1. Generate n sorted random numbers -> Array
 2. Display Array
 3. Search for a key using Binary Search
 4. Search for a key using Ternary Search
 5. Step/frequency count for BEST case (key present, minimum comparisons)
 6. Step/frequency count for WORST case (key absent / last comparison)
 7. Step/frequency count comparison table across increasing n
 0. Exit
========================================================================
"""

    while True:
        print(menu365)
        choice365 = input("Enter your choice: ").strip()

        if choice365 == "1":
            n365 = int(input("Enter number of elements (n): "))
            current_array_365 = generate_array_365(n365)
            print("Sorted array generated successfully.")

        elif choice365 == "2":
            display_array_365(current_array_365)

        elif choice365 == "3":
            if current_array_365 is None:
                print("Generate an array first (option 1).")
                continue
            key365 = int(input("Enter key to search: "))
            start365 = time.perf_counter()
            index365, steps365 = binary_search_365(current_array_365, key365)
            elapsed365 = time.perf_counter() - start365
            if index365 != -1:
                print(f"Found {key365} at index {index365} in {steps365} steps ({elapsed365:.8f} s).")
            else:
                print(f"{key365} not found. Search took {steps365} steps ({elapsed365:.8f} s).")

        elif choice365 == "4":
            if current_array_365 is None:
                print("Generate an array first (option 1).")
                continue
            key365 = int(input("Enter key to search: "))
            start365 = time.perf_counter()
            index365, steps365 = ternary_search_365(current_array_365, key365)
            elapsed365 = time.perf_counter() - start365
            if index365 != -1:
                print(f"Found {key365} at index {index365} in {steps365} steps ({elapsed365:.8f} s).")
            else:
                print(f"{key365} not found. Search took {steps365} steps ({elapsed365:.8f} s).")

        elif choice365 == "5":
            best_case_365(current_array_365)

        elif choice365 == "6":
            worst_case_365(current_array_365)

        elif choice365 == "7":
            comparison_table_365()

        elif choice365 == "0":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
