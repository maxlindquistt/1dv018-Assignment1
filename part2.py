import glob
import math
import os
import random
import time

import matplotlib.pyplot as plt


def bubblesort(lst):
    sorted_list = lst.copy()
    n = len(sorted_list)
    for i in range(n-1):
        swapped = False
        for j in range(n-i-1):
            if sorted_list[j] > sorted_list[j+1]:
                sorted_list[j], sorted_list[j+1] = (
                    sorted_list[j+1], sorted_list[j]
                )
                swapped = True
        if not swapped:
            break
    return sorted_list


def selectionsort(lst):
    sorted_list = lst.copy()
    n = len(sorted_list)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if sorted_list[j] < sorted_list[min_index]:
                min_index = j
        min_value = sorted_list.pop(min_index)
        sorted_list.insert(i, min_value)
    return sorted_list


def insertionsort(lst):
    sorted_list = lst.copy()
    n = len(sorted_list)
    for i in range(1, n):
        insert_index = i
        current_value = sorted_list.pop(i)
        for j in range(i-1, -1, -1):
            if sorted_list[j] > current_value:
                insert_index = j
        sorted_list.insert(insert_index, current_value)
    return sorted_list


def mergesort(lst):
    sorted_list = lst.copy()
    if len(sorted_list) <= 1:
        return sorted_list
    mid = len(sorted_list) // 2
    left_half = mergesort(sorted_list[:mid])
    right_half = mergesort(sorted_list[mid:])
    return merge(left_half, right_half)


def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def partition(lst, low, high):
    pivot = lst[high]
    i = low - 1
    for j in range(low, high):
        if lst[j] <= pivot:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    return i + 1


def quicksort(lst, low=0, high=None):
    if high is None:
        lst = lst.copy()
        high = len(lst) - 1
    if low < high:
        pivot_index = partition(lst, low, high)
        quicksort(lst, low, pivot_index - 1)
        quicksort(lst, pivot_index + 1, high)
    return lst


def _radixsort_nonneg(lst):
    radixArray = [[], [], [], [], [], [], [], [], [], []]
    sorted_list = lst.copy()
    if not sorted_list:
        return sorted_list
    max_num = max(sorted_list)
    exp = 1
    while max_num // exp > 0:
        while len(sorted_list) > 0:
            value = sorted_list.pop()
            radixIndex = (value // exp) % 10
            radixArray[radixIndex].append(value)

        for bucket in radixArray:
            while len(bucket) > 0:
                sorted_list.append(bucket.pop())

        exp *= 10
    return sorted_list


def radixsort(lst):
    negatives = [-x for x in lst if x < 0]
    non_negatives = [x for x in lst if x >= 0]

    sorted_negatives = [-x for x in reversed(_radixsort_nonneg(negatives))]
    sorted_non_negatives = _radixsort_nonneg(non_negatives)

    return sorted_negatives + sorted_non_negatives


def bucketsort(lst):
    num_buckets = len(lst)
    min_value, max_value = min(lst), max(lst)
    if min_value == max_value:
        return lst.copy()
    buckets = [[] for _ in range(num_buckets)]
    value_range = max_value - min_value
    for num in lst:
        index = (num - min_value) * (num_buckets - 1) // value_range
        buckets[index].append(num)
    sorted_list = []
    for bucket in buckets:
        sorted_list.extend(sorted(bucket))
    return sorted_list


def random_input(n):
    return [random.randint(-10 * n, 10 * n) for _ in range(n)]


def lin_reg(x, y):
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    num = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
    den = sum((xi - x_mean) ** 2 for xi in x)
    k = num / den
    m = y_mean - k * x_mean
    return m, k


def time_trial(func, n):
    lst = random_input(n)
    start = time.perf_counter()
    func(lst)
    return time.perf_counter() - start


def log_spaced_sizes(n_low, n_high, count=15):
    sizes = set()
    for i in range(count):
        frac = i / (count - 1)
        n = round(n_low * (n_high / n_low) ** frac)
        sizes.add(n)
    return sorted(sizes)


SQUARE_ALGORITHMS = {
    "Bubble Sort": bubblesort,
    "Selection Sort": selectionsort,
    "Insertion Sort": insertionsort,
}

NLOGN_ALGORITHMS = {
    "Merge Sort": mergesort,
    "Quick Sort": quicksort,
}

SPECIAL_ALGORITHMS = {
    "Merge Sort": mergesort,
    "Quick Sort": quicksort,
    "Radix Sort": radixsort,
    "Bucket Sort": bucketsort,
}


def average_time(func, sizes, repeats=3):
    return [
        sum(time_trial(func, n) for _ in range(repeats)) / repeats
        for n in sizes
    ]


def analyze_group(algorithms, output_dir, complexity_label, n_low, n_high):
    os.makedirs(output_dir, exist_ok=True)
    for old_png in glob.glob(os.path.join(output_dir, "*.png")):
        os.remove(old_png)

    sizes = log_spaced_sizes(n_low, n_high)
    print(f"Input sizes: {sizes}")

    results = {}
    for name, func in algorithms.items():
        print(f"\n=== {name} ===")
        results[name] = average_time(func, sizes)

    plt.figure()
    for name, averages in results.items():
        plt.plot(sizes, averages, marker="o", label=name)
    plt.xlabel("n")
    plt.ylabel("Average time (s)")
    plt.title(f"Figure 1: comparison of {complexity_label} sorting algorithms")
    plt.legend()
    plt.ticklabel_format(style="plain", axis="x")
    plt.savefig(os.path.join(output_dir, "sort_comparison.png"))

    plt.figure()
    log_n = [math.log(n) for n in sizes]
    for name, averages in results.items():
        log_t = [math.log(t) for t in averages]
        m, k = lin_reg(log_n, log_t)
        print(f"{name}: estimated time complexity exponent k = {k:.3f}")
        points = plt.scatter(log_n, log_t, label=f"{name} measured")
        fit_y = [m + k * x for x in log_n]
        plt.plot(
            log_n, fit_y,
            color=points.get_facecolor()[0], label=f"{name} k = {k:.2f}",
        )
    plt.xlabel("log(n)")
    plt.ylabel("log(time)")
    plt.title("Figure 2: log-log fit for sorting algorithms")
    plt.legend()
    plt.savefig(os.path.join(output_dir, "sort_log_log_fit.png"))


if __name__ == "__main__":
    # Sizes below were picked by hand so each group's runtime falls
    # roughly between 0.1s and 2.5s on my personal machine; adjust if needed.
    print("\n### O(n^2) sorts ###")
    analyze_group(
        SQUARE_ALGORITHMS, "O(n²)", "O(n^2)", n_low=3800, n_high=11400
    )

    print("\n### O(n log n) sorts ###")
    analyze_group(
        NLOGN_ALGORITHMS, "O(n ⋅ log(n))", "O(n log n)",
        n_low=130000, n_high=1460000,
    )

    print("\n### special-case sorts ###")
    analyze_group(
        SPECIAL_ALGORITHMS, "special case", "special-case",
        n_low=230000, n_high=1300000,
    )
