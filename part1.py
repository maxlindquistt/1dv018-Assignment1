import glob
import math
import os
import random
import time

import matplotlib.pyplot as plt


def random_input(n):
    return [random.randint(-10 * n, 10 * n) for _ in range(n)]


def threesum_brute(lst, target):
    result = set()
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            for k in range(j + 1, len(lst)):
                if lst[i] + lst[j] + lst[k] == target:
                    result.add(tuple(sorted([lst[i], lst[j], lst[k]])))
    return result


def threesum_pointer(lst, target):
    result = set()
    lst = sorted(lst)
    for i in range(len(lst)):
        left = i + 1
        right = len(lst) - 1
        while left < right:
            current_sum = lst[i] + lst[left] + lst[right]
            if current_sum == target:
                result.add((lst[i], lst[left], lst[right]))
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    return result


def lin_reg(x, y):
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    num = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
    den = sum((xi - x_mean) ** 2 for xi in x)
    k = num / den
    m = y_mean - k * x_mean
    return m, k


def time_trial(func, n, target=0):
    lst = random_input(n)
    start = time.perf_counter()
    func(lst, target)
    return time.perf_counter() - start


def log_spaced_sizes(n_low, n_high, count=15):
    sizes = set()
    for i in range(count):
        frac = i / (count - 1)
        n = round(n_low * (n_high / n_low) ** frac)
        sizes.add(n)
    return sorted(sizes)


def analyze(func, name, n_low, n_high, repeats=3):
    print(f"\n=== {name} ===")
    sizes = log_spaced_sizes(n_low, n_high)
    print(f"Input sizes: {sizes}")

    runs = [[time_trial(func, n) for n in sizes] for _ in range(repeats)]
    averages = [
        sum(run[i] for run in runs) / repeats for i in range(len(sizes))
    ]

    plt.figure()
    for r, run in enumerate(runs, start=1):
        plt.plot(sizes, run, marker="o", label=f"Run {r}")
    plt.xlabel("n")
    plt.ylabel("Time (s)")
    plt.title(f"Figure 1: {name} - execution time per run")
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, f"time_per_run_{name}.png"))

    plt.figure()
    plt.plot(sizes, averages, marker="o")
    plt.xlabel("n")
    plt.ylabel("Average time (s)")
    plt.title(f"Figure 1a: {name} - average execution time ({repeats} runs)")
    plt.savefig(os.path.join(OUTPUT_DIR, f"average_time_{name}.png"))

    log_n = [math.log(n) for n in sizes]
    log_t = [math.log(t) for t in averages]
    m, k = lin_reg(log_n, log_t)
    print(f"Estimated time complexity exponent k = {k:.3f}")

    plt.figure()
    plt.scatter(log_n, log_t, label="Measured")
    fit_y = [m + k * x for x in log_n]
    plt.plot(log_n, fit_y, color="red", label=f"Fit: y = {m:.2f} + {k:.2f}x")
    plt.xlabel("log(n)")
    plt.ylabel("log(time)")
    plt.title(f"Figure 2b: {name} - log-log fit")
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, f"log_log_fit_{name}.png"))

    return sizes, runs, averages, m, k


OUTPUT_DIR = "3-sum"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for old_png in glob.glob(os.path.join(OUTPUT_DIR, "*.png")):
        os.remove(old_png)

    print("=== Correctness check: 3 random lists of size 15 ===")
    for i in range(1, 4):
        demo_list = random_input(15)
        print(f"\nList {i}: {demo_list}")
        print(f"Triples: {threesum_brute(demo_list, 0)}")

    # Sizes below were picked by hand so each algorithm's runtime falls
    # roughly between 0.1s and 5s on my personal machine; adjust if needed.
    analyze(threesum_brute, "brute_force", n_low=200, n_high=1000)
    analyze(threesum_pointer, "two_pointer", n_low=2000, n_high=14500)
