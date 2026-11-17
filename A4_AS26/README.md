# CSF302 Assignment 4: Booking the Hall

A community hall in Paro takes booking requests `(start, finish, fee)`, and only one event can use it at a time. The manager accepts the request that ends earliest. This project checks whether that earns the most money, and finds the schedule that does.

| Function | Method | Time |
|---|---|---|
| `greedy_earliest_finish` | Greedy: earliest finish first | O(n log n) |
| `greedy_highest_fee` | Greedy: highest fee first | O(n²) |
| `best_schedule` | Dynamic programming: `OPT(j) = max(OPT(j-1), fee_j + OPT(p(j)))` | O(n log n) |
| `brute_force` | Tries every subset (for checking, n ≤ 15) | O(2ⁿ · n²) |

Each function returns `(total_fee, chosen)`, where `chosen` is the sorted list of accepted request indices.

## Files

| File | What it is |
|---|---|
| `booking.py` | The four functions (Part A) and the analysis (Part C) |
| `test_booking.py` | Tests, including DP vs brute force on 1,000 random inputs (Part B) |
| `CSF302_02240365_A4.pdf` | Report: counterexamples, DP explanation, ratio table, complexities, reflection |

## How to run

Requires Python 3. The analysis also needs matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install matplotlib
```

Run the tests:

```bash
python test_booking.py
```

Run the analysis. This prints the example, the counterexamples and the ratio table, and saves `ratio_histogram.png`:

```bash
python booking.py
```

## Example

```python
from booking import greedy_earliest_finish, best_schedule

requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]
print(greedy_earliest_finish(requests))   # (7500, [0, 3, 4])
print(best_schedule(requests))            # (10000, [1, 4])
```

## Results

Over 1,000 random days of 50 requests:

| Rule | Average of optimal | Worst |
|---|---|---|
| Earliest finish | 78.3% | 35.7% |
| Highest fee | 80.2% | 35.2% |

Neither greedy rule is optimal when fees differ. `best_schedule` always is, and it is just as fast.

## AI use

Claude (Anthropic) was used to help structure the code, suggest test cases and improve the report wording. All code was run and `best_schedule` was checked against `brute_force`.
