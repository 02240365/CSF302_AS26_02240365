"""
CSF302 Assignment 2 - Part B: Tests

Run with:   python test_closest.py -v      (or: pytest -v test_closest.py)
"""

import math
import random
import unittest

from closest import closest_pair, closest_pair_brute, dist


class TestClosestPair(unittest.TestCase):

    def check_valid(self, points, result):
        """A result (d, i, j) is valid if i < j and d really is
        the distance between points[i] and points[j]."""
        d, i, j = result
        self.assertLess(i, j)
        self.assertTrue(0 <= i < len(points) and 0 <= j < len(points))
        self.assertAlmostEqual(d, dist(points[i], points[j]))

    def compare(self, points):
        """Divide and conquer must give the same distance as brute force.
        (If two pairs tie, the indices may differ, so we compare d and
        check that the returned pair is valid.)"""
        dc = closest_pair(points)
        bf = closest_pair_brute(points)
        self.assertAlmostEqual(dc[0], bf[0])
        self.check_valid(points, dc)
        self.check_valid(points, bf)
        return dc

    # ---------- B.1  500+ random inputs of 2 to 50 points ----------
    def test_random_against_brute(self):
        rng = random.Random(2024)
        for trial in range(1000):                     # 1000 >= 500
            n = rng.randint(2, 50)
            # small grid sometimes, so ties and duplicates also appear
            size = rng.choice([10, 100, 10**6])
            pts = [(rng.randint(0, size), rng.randint(0, size)) for _ in range(n)]
            with self.subTest(trial=trial, n=n):
                self.compare(pts)

    def test_random_float_points(self):
        rng = random.Random(7)
        for trial in range(500):
            n = rng.randint(2, 50)
            pts = [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(n)]
            with self.subTest(trial=trial):
                self.compare(pts)

    # ---------- Example from the assignment sheet ----------
    def test_assignment_example(self):
        pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        d, i, j = closest_pair(pts)
        self.assertAlmostEqual(d, math.sqrt(2))       # 1.414...
        self.assertEqual((i, j), (0, 5))              # (2,3) and (3,4)

    # ---------- B.2  Edge cases ----------
    def test_exactly_two_points(self):
        pts = [(0, 0), (3, 4)]
        self.assertEqual(closest_pair(pts), (5.0, 0, 1))
        self.assertEqual(closest_pair_brute(pts), (5.0, 0, 1))

    def test_duplicate_points_give_zero(self):
        pts = [(5, 5), (1, 9), (7, 2), (1, 9), (8, 8)]
        d, i, j = closest_pair(pts)
        self.assertEqual(d, 0.0)
        self.assertEqual((i, j), (1, 3))
        # many duplicates of the same point
        self.assertEqual(closest_pair([(4, 4)] * 10)[0], 0.0)

    def test_all_on_one_vertical_line(self):
        # every point has the same x, so the dividing line passes
        # through all of them
        pts = [(3, y) for y in [0, 10, 25, 26, 40, 70, 71.5, 90]]
        d, i, j = self.compare(pts)
        self.assertEqual(d, 1.0)
        self.assertEqual((i, j), (2, 3))

    def test_closest_pair_across_dividing_line(self):
        # Two clusters far apart; the closest two points sit either side
        # of the middle x (the dividing line), so only the strip finds them.
        left = [(0, 0), (0, 100), (0, 200), (49, 50)]
        right = [(50, 50), (100, 0), (100, 100), (100, 200)]
        pts = left + right
        d, i, j = self.compare(pts)
        self.assertEqual(d, 1.0)
        self.assertEqual((i, j), (3, 4))              # (49,50) and (50,50)

    def test_larger_random_against_brute(self):
        # one bigger check so the recursion goes several levels deep
        rng = random.Random(1)
        pts = [(rng.random(), rng.random()) for _ in range(2000)]
        self.compare(pts)

    def test_too_few_points(self):
        with self.assertRaises(ValueError):
            closest_pair([(1, 1)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
