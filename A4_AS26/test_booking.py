"""
CSF302 Assignment 4 - Part B: Tests

Run with:   python test_booking.py      (or: pytest -v test_booking.py)
"""

import random
import unittest

from booking import (greedy_earliest_finish, greedy_highest_fee,
                     best_schedule, brute_force, fits, EXAMPLE,
                     CE_EARLIEST, CE_HIGHEST)

ALL = [greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force]


def random_requests(n, rng, equal_fee=False):
    reqs = []
    for _ in range(n):
        s = rng.randint(0, 20)
        fee = 100 if equal_fee else rng.randint(1, 50)
        reqs.append((s, s + rng.randint(1, 6), fee))
    return reqs


class TestBooking(unittest.TestCase):

    def check_valid(self, reqs, result):
        """A result is valid if its indices are sorted and distinct, the
        chosen requests do not overlap, and the total equals their fees."""
        total, chosen = result
        self.assertEqual(chosen, sorted(set(chosen)))
        for a in chosen:
            for b in chosen:
                if a < b:
                    self.assertTrue(fits(reqs[a], reqs[b]), f"{a} and {b} overlap")
        self.assertEqual(total, sum(reqs[i][2] for i in chosen))

    # ---------- B.1  best_schedule vs brute_force, 500+ random inputs ----------
    def test_dp_matches_brute_force(self):
        rng = random.Random(1)
        for trial in range(1000):                    # 1000 >= 500
            reqs = random_requests(rng.randint(0, 10), rng)
            with self.subTest(trial=trial):
                dp, bf = best_schedule(reqs), brute_force(reqs)
                self.assertEqual(dp[0], bf[0])       # same optimal total
                for f in ALL:                        # every answer is a real schedule
                    self.check_valid(reqs, f(reqs))
                    self.assertLessEqual(f(reqs)[0], bf[0])

    # ---------- B.2  Edge cases ----------
    def test_no_requests(self):
        for f in ALL:
            self.assertEqual(f([]), (0, []))

    def test_one_request(self):
        for f in ALL:
            self.assertEqual(f([(9, 12, 500)]), (500, [0]))

    def test_all_overlapping(self):
        reqs = [(9, 17, 300), (10, 16, 900), (11, 15, 500), (12, 14, 700)]
        self.assertEqual(best_schedule(reqs), (900, [1]))       # only one can be taken
        self.assertEqual(brute_force(reqs), (900, [1]))

    def test_none_overlapping(self):
        reqs = [(14, 15, 200), (8, 9, 100), (10, 12, 300)]
        for f in ALL:
            self.assertEqual(f(reqs), (600, [0, 1, 2]))         # take everything

    def test_back_to_back(self):
        # ending at 12 and starting at 12 both fit
        reqs = [(9, 12, 100), (12, 14, 100), (14, 17, 100)]
        for f in ALL:
            self.assertEqual(f(reqs), (300, [0, 1, 2]))

    # ---------- B.3  Equal fees: earliest finish is always optimal ----------
    def test_equal_fees_greedy_is_optimal(self):
        rng = random.Random(2)
        for trial in range(1000):
            reqs = random_requests(rng.randint(0, 12), rng, equal_fee=True)
            with self.subTest(trial=trial):
                self.assertEqual(greedy_earliest_finish(reqs)[0], best_schedule(reqs)[0])

    # ---------- Examples from the brief and Part C ----------
    def test_brief_example(self):
        self.assertEqual(greedy_earliest_finish(EXAMPLE), (7500, [0, 3, 4]))
        self.assertEqual(best_schedule(EXAMPLE), (10000, [1, 4]))

    def test_counterexamples(self):
        self.assertLess(greedy_earliest_finish(CE_EARLIEST)[0], best_schedule(CE_EARLIEST)[0])
        self.assertLess(greedy_highest_fee(CE_HIGHEST)[0], best_schedule(CE_HIGHEST)[0])

    def test_dp_on_large_input(self):
        # 50 requests: too many for brute force, so check DP gives a valid
        # schedule that is at least as good as both greedy rules
        rng = random.Random(3)
        for _ in range(200):
            reqs = random_requests(50, rng)
            best = best_schedule(reqs)
            self.check_valid(reqs, best)
            self.assertGreaterEqual(best[0], greedy_earliest_finish(reqs)[0])
            self.assertGreaterEqual(best[0], greedy_highest_fee(reqs)[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
