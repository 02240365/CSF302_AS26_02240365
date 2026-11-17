"""
CSF302 Assignment 3 - Part B: Tests

Run with:   python test_sorts.py      (or: pytest -v test_sorts.py)
sorted() is used here ONLY to check the answers.
"""

import random
import unittest

from sorts import quicksort_basic, quicksort_improved

SORTS = [("basic", quicksort_basic), ("improved", quicksort_improved)]


class TestSorts(unittest.TestCase):

    def check(self, data):
        """Both sorts must give exactly the same result as sorted(),
        and must sort the list in place."""
        for name, sort in SORTS:
            a = list(data)
            sort(a)
            self.assertEqual(a, sorted(data), f"{name} failed on {data}")

    # ---------- B.1  At least 500 random lists ----------
    def test_random_lists(self):
        rng = random.Random(2024)
        for trial in range(1000):                       # 1000 >= 500
            n = rng.randint(0, 200)
            data = [rng.randint(-1000, 1000) for _ in range(n)]
            with self.subTest(trial=trial):
                self.check(data)

    def test_random_lists_different_cutoffs(self):
        rng = random.Random(7)
        for cutoff in [1, 4, 8, 16, 32, 64]:
            for _ in range(100):
                data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 150))]
                a = list(data)
                quicksort_improved(a, cutoff)
                self.assertEqual(a, sorted(data))

    # ---------- B.2  Edge cases ----------
    def test_empty_list(self):
        self.check([])

    def test_one_element(self):
        self.check([42])

    def test_all_equal(self):
        self.check([7] * 50)

    def test_already_sorted(self):
        self.check(list(range(300)))

    def test_reverse_sorted(self):
        self.check(list(range(300, 0, -1)))

    def test_negative_numbers(self):
        self.check([-5, 3, -1, 0, -100, 99, -5, 2])

    # ---------- The real-data problem ----------
    def test_improved_on_large_sorted_input(self):
        # 100,000 sorted items: the basic version would crash here,
        # the improved version must sort it with no RecursionError.
        data = list(range(100_000))
        a = list(data)
        quicksort_improved(a)
        self.assertEqual(a, data)

    def test_improved_on_many_duplicates(self):
        rng = random.Random(1)
        data = [rng.choice([100, 500]) for _ in range(50_000)]   # Nu 100 / Nu 500
        a = list(data)
        quicksort_improved(a)
        self.assertEqual(a, sorted(data))


if __name__ == "__main__":
    unittest.main(verbosity=2)
