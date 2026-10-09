# Assignment 1 — Report

## Part 1 — 3-SUM (`part1.py`)

### 1. How the experiments were conducted

We compared two ways of solving 3-SUM (finding all triples in a list that add up to `0`):

- **Brute force** — three nested loops that check every possible triple.
- **Two-pointer** — sorts the list once, then finds triples with a smarter linear scan.

For each one, we hand-picked a size range (based on a few quick trial runs) so the runtime would land roughly between 0.1 and 5 seconds (too small and the timer is noisy, too big and it takes forever), then generated 15 sizes spread evenly on a log scale within that range. Each size was run 3 times with a new random list each time, and we used the average of those 3 runs.

### 2. Results and comparison

The brute-force version needed sizes around 200–1000 to reach that time range, while the two-pointer version needed sizes around 2000–14 500 — a clear sign it's much faster for the same input size.

![Brute force — average time](<3-sum/average_time_brute_force.png>)
![Two-pointer — average time](<3-sum/average_time_two_pointer.png>)

### 3. How we arrived at the results

If runtime grows like `T(n) = c · n^k`, taking the log of both sides gives a straight line:

```
log(T) = log(c) + k · log(n)
```

So if we plot `log(n)` against `log(T)` and fit a straight line through the points, the slope of that line is our estimate of `k`, the time-complexity exponent. We fit this line with ordinary linear regression (least squares).

- **Brute force:** k ≈ **3.1** → matches the expected O(n³).
- **Two-pointer:** k ≈ **2.0** → matches the expected O(n²).

![Brute force — log-log fit](<3-sum/log_log_fit_brute_force.png>)
![Two-pointer — log-log fit](<3-sum/log_log_fit_two_pointer.png>)

### 4. How the two-pointer approach works

1. Sort the list.
2. Fix one number, `lst[i]`.
3. Use two pointers — one starting right after `i`, one at the end of the list — and check what the three numbers add up to:
   - Sum too small → move the left pointer right.
   - Sum too big → move the right pointer left.
   - Sum matches → we found a triple; move both pointers inward and keep going.
4. Repeat for every `i`.

Because sorting lets us tell instantly whether the sum is too big or too small, we never need to check every pair — the two pointers sweep through the list once per `i`, which is why this is O(n²) instead of O(n³).

---

## Part 2 — Sorting algorithms (`part2.py`)

### 1. How the experiments were conducted

Seven sorting algorithms were grouped by expected complexity and each group was timed the same way as Part 1 (hand-picked size range, 15 log-spaced sizes, 3 repeats, average taken):

- **O(n²) group:** Bubble Sort, Selection Sort, Insertion Sort.
- **O(n log n) group:** Merge Sort, Quick Sort.
- **Special-case group:** Merge Sort and Quick Sort compared against Radix Sort and Bucket Sort, two algorithms that don't compare elements directly.

For a group, all algorithms in it were timed on the *same* input sizes, so the comparison is fair.

### 2. Results and comparison

**O(n²) group** — all three land around k ≈ 2, but Bubble Sort is clearly the slowest in practice since it swaps elements far more often than the other two.

![O(n²) comparison](<O(n²)/sort_comparison.png>)

**O(n log n) vs. special case** — Merge Sort, Quick Sort, Radix Sort and Bucket Sort were all compared together. Bucket Sort came out fastest, followed by Quick Sort and Merge Sort, with Radix Sort the slowest of the four (its cost grows with how many digits the numbers have, and our numbers get bigger as the list gets longer).

| Algorithm | k (measured) |
|---|---|
| Merge Sort | ~1.15 |
| Quick Sort | ~1.20 |
| Radix Sort | ~1.6 |
| Bucket Sort | ~1.2 |

![Special case comparison](<special case/sort_comparison.png>)
![Special case log-log fit](<special case/sort_log_log_fit.png>)

### 3. How we arrived at the results

Same method as Part 1: plot `log(n)` vs. `log(average time)` and fit a straight line; the slope is the estimated exponent `k`. All the O(n²) sorts fit close to k = 2. The other four fit well below that, close to k = 1, confirming they scale much better than the O(n²) group — even though `n · log(n)` isn't a perfectly straight line on a log-log plot, so the fitted k ends up a bit above 1 rather than exactly 1.

### 4. How each algorithm works

- **Bubble Sort** — repeatedly swaps neighbouring elements that are in the wrong order, pushing the largest value to the end each pass. Stops early once a pass makes no swaps.
- **Selection Sort** — repeatedly finds the smallest remaining value and moves it to its correct position.
- **Insertion Sort** — builds up a sorted section at the front one element at a time, inserting each new element where it belongs.
- **Merge Sort** — splits the list in half again and again until each piece has one element, then merges the pieces back together in sorted order.
- **Quick Sort** — picks a pivot value, rearranges the list so smaller values are before it and bigger values after it, then repeats on each side.
- **Radix Sort** — sorts numbers digit by digit (starting from the last digit), using counting to group numbers with the same digit together, without ever comparing two numbers directly.
- **Bucket Sort** — spreads the numbers into several "buckets" based on their value, sorts each small bucket individually, then joins the buckets back together in order.
