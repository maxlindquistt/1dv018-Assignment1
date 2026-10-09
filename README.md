# Assignment 1

Experiments on algorithm time complexity: the 3-SUM problem and sorting algorithms.

## Requirements

- Python 3
- matplotlib (`pip install matplotlib`)

## Files

| File | What it does |
|---|---|
| `part1.py` | 3-SUM: brute force vs. two-pointer. Checks correctness, then times both and estimates their complexity. |
| `part2.py` | Sorting: Bubble, Selection, Insertion, Merge, Quick, Radix, and Bucket sort, grouped and timed by complexity class. |
| `report.md` / `report.pdf` | Write-up explaining the method, results, and the math behind the complexity estimates. |

## How to run

```
python3 part1.py
python3 part2.py
```

Each script prints its results to the terminal and saves plots as PNGs — no need to close any windows. A full run of `part2.py` takes a few minutes since it times algorithms on large inputs.

## Output folders

- `3-sum/` — plots for the two 3-SUM algorithms
- `O(n²)/` — Bubble, Selection, Insertion sort comparison
- `O(n ⋅ log(n))/` — Merge vs. Quick sort comparison
- `special case/` — Radix and Bucket sort compared against Merge and Quick sort

Each folder contains a running-time plot and a log-log plot with a fitted line used to estimate the time complexity.
