# CSF302 Assignment 3: Fixing a Slow Quicksort

A textbook quicksort is slow or crashes (`RecursionError`) on real bank data that is often already sorted and full of repeated amounts. This project shows why and fixes it.

- `quicksort_basic(a)`: Lomuto partition with the last element as pivot
- `quicksort_improved(a, cutoff=16)`: random pivot, insertion sort for small parts, recursion on the smaller part only (depth at most log₂ n), and a 3-way partition for repeated values

Both sort the list in place and do not use `sorted()` or `list.sort()`.

## Files

| File | What it is |
|---|---|
| `sorts.py` | Both sorts (Part A) and the timing experiments (Part C) |
| `test_sorts.py` | Tests against `sorted()`, plus edge cases (Part B) |
| `CSF302_02240365_A3.pdf` | Report: timing tables and graphs, recurrence, cutoff, comparison with `sorted()`, reflection |

## How to run

Requires Python 3. The timing experiment also needs matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install matplotlib
```

Run the tests:

```bash
python test_sorts.py
```

Run the timing experiments (under a minute). This prints the tables, the cutoff results and the `sorted()` comparison, and saves `timing_graphs.png` and `cutoff_graph.png`:

```bash
python sorts.py
```

## Example

```python
from sorts import quicksort_improved

a = [500, 100, 100, 500, 100]
quicksort_improved(a)
print(a)   # [100, 100, 100, 500, 500]
```

## Results

- `quicksort_basic` crashes on every sorted input, and on many duplicates (values 0 to 9) from n = 16,000
- `quicksort_improved` never crashes and is Θ(n log n) on all three input types
- Best cutoff for n = 100,000 random values: 16
- `sorted()` is still about 9× faster, mostly because it is written in C

## AI use

Claude (Anthropic) was used to help structure the code, suggest test cases and improve the report wording. All code was run and checked against `sorted()`.
