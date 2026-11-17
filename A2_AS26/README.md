# CSF302 Assignment 2: Closest Camera Traps

Finds the closest pair of camera traps on a map grid in two ways:

- **Brute force**: checks every pair, Θ(n²)
- **Divide and conquer**: sorts, splits, solves each half, then checks the strip around the dividing line, Θ(n log n)

Both functions return `(d, i, j)`: the smallest distance `d` and the indices `i < j` of the two points.

## Files

| File | What it is |
|---|---|
| `closest.py` | Both algorithms (Part A) and the timing experiment (Part C) |
| `test_closest.py` | Tests comparing the two versions, plus edge cases (Part B) |
| `CSF302_02240365_A2.pdf` | Report: recurrence, timing table, graph, crossover point, reflection |

## How to run

Requires Python 3. The timing experiment also needs matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install matplotlib
```

Run the tests:

```bash
python test_closest.py
```

Run the timing experiment (about 5 minutes; it prints the table and crossover, and saves `timing_loglog.png`):

```bash
python closest.py
```

## Example

```python
from closest import closest_pair

points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
print(closest_pair(points))   # (1.414..., 0, 5) -> points (2, 3) and (3, 4)
```

## Results

| n | Brute force (s) | Divide and conquer (s) |
|---|---|---|
| 1,000 | 0.052 | 0.0020 |
| 16,000 | 11.716 | 0.0456 |
| 64,000 | 196.552 (over 60 s limit) | 0.2657 |

- Recurrence: T(n) = 2T(n/2) + cn, which gives Θ(n log n) by the Master Method (Case 2)
- Divide and conquer is faster from **n = 19** on my machine
- All 9 tests pass

## AI use

Claude (Anthropic) was used to help plan the code, suggest test cases and improve the report wording. All code was run and checked against the brute-force version.