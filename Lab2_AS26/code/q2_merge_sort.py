"""
CSF302 - Lab 2
Q2: Merge Sort Analysis (Menu-Driven Program)

WHAT THIS PROGRAM DOES
-----------------------
A menu-driven program that:
  1. Generates n random numbers into an array
  2. Displays the array
  3. Sorts the array in ASCENDING order using Merge Sort
  4. Sorts the array in DESCENDING order (Bubble Sort used here, any
     sorting algorithm is allowed by the instructions)
  5. Shows Merge Sort step/frequency count + timing on RANDOM data
  6. Shows Merge Sort step/frequency count + timing on ALREADY SORTED data
  7. Shows Merge Sort step/frequency count + timing on DESCENDING-SORTED data
  0. Exit

Every sort keeps a running "comparison count" (step/frequency count) so
we can compare how the input arrangement (random / sorted / reverse
sorted) affects the number of operations Merge Sort performs.
"""

import random
import time
import matplotlib.pyplot as plt

# a single global counter, reset before every sort, used to record the
# step/frequency count (number of element comparisons) of Merge Sort
comparison_count_365 = 0


# ---------------------------------------------------------------------
# MERGE SORT (ascending) with step/frequency counting
# ---------------------------------------------------------------------
def merge_365(arr365, left365, mid365, right365):
    """Merge two sorted halves arr365[left365:mid365+1] and arr365[mid365+1:right365+1]."""
    global comparison_count_365

    left_part365 = arr365[left365:mid365 + 1]
    right_part365 = arr365[mid365 + 1:right365 + 1]

    i365 = j365 = 0
    k365 = left365

    while i365 < len(left_part365) and j365 < len(right_part365):
        comparison_count_365 += 1              # one comparison step
        if left_part365[i365] <= right_part365[j365]:
            arr365[k365] = left_part365[i365]
            i365 += 1
        else:
            arr365[k365] = right_part365[j365]
            j365 += 1
        k365 += 1

    while i365 < len(left_part365):             # copy any leftovers
        arr365[k365] = left_part365[i365]
        i365 += 1
        k365 += 1

    while j365 < len(right_part365):
        arr365[k365] = right_part365[j365]
        j365 += 1
        k365 += 1


def merge_sort_365(arr365, left365, right365):
    """Recursively split and merge -> classic O(n log n) Merge Sort."""
    if left365 < right365:
        mid365 = (left365 + right365) // 2
        merge_sort_365(arr365, left365, mid365)
        merge_sort_365(arr365, mid365 + 1, right365)
        merge_365(arr365, left365, mid365, right365)


def run_merge_sort_with_count_365(arr365):
    """Reset the global counter, run merge sort, return (steps, time_taken)."""
    global comparison_count_365
    comparison_count_365 = 0
    working_copy365 = arr365.copy()

    start365 = time.perf_counter()
    merge_sort_365(working_copy365, 0, len(working_copy365) - 1)
    elapsed365 = time.perf_counter() - start365

    return working_copy365, comparison_count_365, elapsed365


# ---------------------------------------------------------------------
# DESCENDING SORT - Bubble Sort (any algorithm is allowed for option 4)
# ---------------------------------------------------------------------
def bubble_sort_descending_365(arr365):
    """Sort arr365 into DESCENDING order using Bubble Sort. Returns steps."""
    steps365 = 0
    n365 = len(arr365)
    result365 = arr365.copy()

    for i365 in range(n365 - 1):
        for j365 in range(n365 - 1 - i365):
            steps365 += 1                       # one comparison step
            if result365[j365] < result365[j365 + 1]:   # swap for descending order
                result365[j365], result365[j365 + 1] = result365[j365 + 1], result365[j365]

    return result365, steps365


# ---------------------------------------------------------------------
# MENU ACTIONS
# ---------------------------------------------------------------------
def generate_array_365(n365):
    return [random.randint(1, 10000) for _ in range(n365)]


def display_array_365(arr365):
    if arr365 is None:
        print("No array generated yet. Choose option 1 first.")
        return
    print(f"Array (size {len(arr365)}):")
    print(arr365 if len(arr365) <= 30 else str(arr365[:30]) + " ... (truncated)")


def time_complexity_test_365(kind365):
    """
    Run Merge Sort on several array sizes for a given data arrangement
    ('random', 'ascending', 'descending'), print a step-count table,
    and plot n vs steps / n vs time.
    """
    sizes365 = [100, 500, 1000, 2000, 4000, 8000]
    steps_list365 = []
    time_list365 = []

    print(f"\n--- Merge Sort Time Complexity: {kind365.upper()} data ---")
    print("{:<10}{:<15}{:<15}".format("n", "Steps", "Time (s)"))
    print("-" * 40)

    for size365 in sizes365:
        base_arr365 = generate_array_365(size365)
        if kind365 == "ascending":
            base_arr365.sort()
        elif kind365 == "descending":
            base_arr365.sort(reverse=True)
        # 'random' -> leave as generated

        _, steps365, elapsed365 = run_merge_sort_with_count_365(base_arr365)
        steps_list365.append(steps365)
        time_list365.append(elapsed365)
        print("{:<10}{:<15}{:<15.6f}".format(size365, steps365, elapsed365))

    plt.figure(figsize=(8, 5))
    plt.plot(sizes365, steps_list365, marker='o', color='tab:blue')
    plt.xlabel('Input size (n)')
    plt.ylabel('Step / Comparison Count')
    plt.title(f'Merge Sort Step Count on {kind365.title()} Data\n(Student No: 02240365)')
    plt.grid(True)
    plt.tight_layout()
    filename365 = f'q2_merge_sort_{kind365}_graph.png'
    plt.savefig(filename365, dpi=150)
    plt.close()
    print(f"Graph saved as '{filename365}'")


# ---------------------------------------------------------------------
# MAIN MENU LOOP
# ---------------------------------------------------------------------
def main():
    current_array_365 = None

    menu365 = """
======================================================================
 CSF302 Lab 2 - Q2: MERGE SORT ANALYSIS (Student No: 02240365)
======================================================================
 1. Generate n random numbers -> Array
 2. Display Array
 3. Sort in Ascending Order using Merge Sort
 4. Sort in Descending Order (Bubble Sort)
 5. Time Complexity: Merge Sort on RANDOM data
 6. Time Complexity: Merge Sort on ALREADY-SORTED (ascending) data
 7. Time Complexity: Merge Sort on DESCENDING-SORTED data
 0. Exit
======================================================================
"""
    while True:
        print(menu365)
        choice365 = input("Enter your choice: ").strip()

        if choice365 == "1":
            n365 = int(input("Enter number of elements (n): "))
            current_array_365 = generate_array_365(n365)
            print("Array generated successfully.")

        elif choice365 == "2":
            display_array_365(current_array_365)

        elif choice365 == "3":
            if current_array_365 is None:
                print("Generate an array first (option 1).")
                continue
            sorted_arr365, steps365, elapsed365 = run_merge_sort_with_count_365(current_array_365)
            current_array_365 = sorted_arr365
            print(f"Sorted (ASCENDING) via Merge Sort in {steps365} steps, "
                  f"{elapsed365:.6f} seconds.")
            display_array_365(current_array_365)

        elif choice365 == "4":
            if current_array_365 is None:
                print("Generate an array first (option 1).")
                continue
            sorted_arr365, steps365 = bubble_sort_descending_365(current_array_365)
            current_array_365 = sorted_arr365
            print(f"Sorted (DESCENDING) via Bubble Sort in {steps365} steps.")
            display_array_365(current_array_365)

        elif choice365 == "5":
            time_complexity_test_365("random")

        elif choice365 == "6":
            time_complexity_test_365("ascending")

        elif choice365 == "7":
            time_complexity_test_365("descending")

        elif choice365 == "0":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    # ------------------------------------------------------------
    # ANALYSIS / CONCLUSION:
    # Merge Sort always performs O(n log n) comparisons regardless of
    # whether the input is random, already sorted, or reverse sorted,
    # because it always splits the array in half and merges, unlike
    # algorithms such as Insertion Sort whose performance depends on
    # the initial order. The step counts recorded for random,
    # ascending and descending inputs are therefore very close to each
    # other for the same n, confirming Merge Sort's stable O(n log n)
    # behaviour in the best, average and worst cases.
    # ------------------------------------------------------------


if __name__ == "__main__":
    main()
