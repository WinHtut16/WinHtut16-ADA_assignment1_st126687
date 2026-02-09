import time
import statistics
import random
import math
import matplotlib.pyplot as plt
import numpy as np

def generate_uniform_dataset(n, D, alpha, seed=None):
    if seed is not None:
        random.seed(seed)
    
    T = alpha * n * D
    intervals = []
    
    for _ in range(n):
        s_i = random.uniform(0, T)
        d_i = random.uniform(1, D)
        f_i = s_i + d_i
        intervals.append((s_i, f_i))
    
    # Sort by start time for consistent output (optional)
    intervals.sort(key=lambda x: x[0])
    return intervals

def greedy_eft(intervals):
    if not intervals:
        return 0, []
    
    # Sort by increasing finish time
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    
    selected = [sorted_intervals[0]]
    last_finish = sorted_intervals[0][1]
    
    for start, finish in sorted_intervals[1:]:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return len(selected), selected

def greedy_est(intervals):
    if not intervals:
        return 0, []
    
    # Sort by increasing start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    selected = [sorted_intervals[0]]
    last_finish = sorted_intervals[0][1]
    
    for start, finish in sorted_intervals[1:]:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return len(selected), selected

def greedy_sd(intervals):
    if not intervals:
        return 0, []
    
    # Sort by increasing duration (finish - start)
    sorted_intervals = sorted(intervals, key=lambda x: x[1] - x[0])
    
    selected = [sorted_intervals[0]]
    last_finish = sorted_intervals[0][1]
    
    for start, finish in sorted_intervals[1:]:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return len(selected), selected

def exhaustive_interval_scheduling(intervals):
    n = len(intervals)
    if n == 0:
        return 0, []
    
    max_size = 0
    max_subset = []
    
    # Enumerate all 2^n subsets using bitmasks
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(intervals[i])
        
        # Sort subset by start time
        subset.sort(key=lambda x: x[0])
        
        # Check if feasible (no overlaps in sorted order)
        feasible = True
        for j in range(1, len(subset)):
            if subset[j-1][1] > subset[j][0]:
                feasible = False
                break
        
        # Update if larger
        if feasible and len(subset) > max_size:
            max_size = len(subset)
            max_subset = subset[:]  # Copy the list
    
    return max_size, max_subset

def time_algorithm(alg_func, intervals, warm_up_runs=1):
    for _ in range(warm_up_runs):
        alg_func(intervals)
    start = time.perf_counter()
    count, _ = alg_func(intervals)
    end = time.perf_counter()
    return end - start, count

def run_big_o_validation():
    D = 10
    alphas = [0.1, 1, 5]
    num_trials = 10
    
    # Greedy setup
    greedy_ns = [2**i for i in range(10, 21)]  # 1024 to 1M
    greedy_algs = {
        'EFT': greedy_eft,
        'EST': greedy_est,
        'SD': greedy_sd
    }
    
    # Exhaustive setup
    exhaustive_ns = list(range(5, 21, 5))  # 5,10,15,20
    
    # Data collectors
    greedy_data = {alpha: {alg: {'ns': greedy_ns, 'mean_times': [], 'std_times': []} for alg in greedy_algs} for alpha in alphas}
    exhaustive_data = {alpha: {'ns': exhaustive_ns, 'mean_times': [], 'std_times': []} for alpha in alphas}
    
    # Run greedy experiments
    for alpha in alphas:
        for n in greedy_ns:
            for alg_name, alg_func in greedy_algs.items():
                times = []
                for trial in range(num_trials):
                    seed = random.randint(0, 1000000)
                    intervals = generate_uniform_dataset(n, D, alpha, seed)
                    t, _ = time_algorithm(alg_func, intervals)
                    times.append(t)
                mean_t = statistics.mean(times)
                std_t = statistics.stdev(times)
                greedy_data[alpha][alg_name]['mean_times'].append(mean_t)
                greedy_data[alpha][alg_name]['std_times'].append(std_t)
    
    # Run exhaustive experiments
    for alpha in alphas:
        for n in exhaustive_ns:
            times = []
            for trial in range(num_trials):
                seed = random.randint(0, 1000000)
                intervals = generate_uniform_dataset(n, D, alpha, seed)
                t, _ = time_algorithm(exhaustive_interval_scheduling, intervals)
                times.append(t)
            mean_t = statistics.mean(times)
            std_t = statistics.stdev(times)
            exhaustive_data[alpha]['mean_times'].append(mean_t)
            exhaustive_data[alpha]['std_times'].append(std_t)
    
    # Plotting for Greedy (one set per regime, combining algs)
    for alpha in alphas:
        plt.figure(figsize=(12, 6))
        
        # Log-log: t(n) vs n
        plt.subplot(1, 2, 1)
        for alg_name in greedy_algs:
            ns = np.array(greedy_ns)
            times = np.array(greedy_data[alpha][alg_name]['mean_times'])
            plt.loglog(ns, times, label=alg_name)
            plt.fill_between(ns, times - greedy_data[alpha][alg_name]['std_times'], times + greedy_data[alpha][alg_name]['std_times'], alpha=0.2)
        plt.xlabel('n (log scale)')
        plt.ylabel('t(n) (log scale)')
        plt.title(f'Runtime vs n (log-log) - alpha={alpha}')
        plt.legend()
        plt.grid(True)
        
        # Normalized: t(n) / (n log2 n)
        plt.subplot(1, 2, 2)
        for alg_name in greedy_algs:
            ns = np.array(greedy_ns)
            times = np.array(greedy_data[alpha][alg_name]['mean_times'])
            log2n = np.log2(ns)
            normalized = times / (ns * log2n)
            plt.plot(ns, normalized, label=alg_name)
        plt.xlabel('n')
        plt.ylabel('t(n) / (n log2 n)')
        plt.title(f'Normalized Runtime - alpha={alpha}')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'greedy_plots_alpha_{alpha}.png')
        plt.close()
    
    # Plotting for Exhaustive
    for alpha in alphas:
        plt.figure(figsize=(12, 6))
        
        # t(n) vs n
        plt.subplot(1, 2, 1)
        ns = np.array(exhaustive_data[alpha]['ns'])
        times = np.array(exhaustive_data[alpha]['mean_times'])
        plt.plot(ns, times, label='Exhaustive')
        plt.fill_between(ns, times - exhaustive_data[alpha]['std_times'], times + exhaustive_data[alpha]['std_times'], alpha=0.2)
        plt.xlabel('n')
        plt.ylabel('t(n)')
        plt.title(f'Runtime vs n - alpha={alpha}')
        plt.legend()
        plt.grid(True)
        
        # Normalized: t(n) / (n 2^n)
        plt.subplot(1, 2, 2)
        normalized = times / (ns * (2 ** ns))
        plt.plot(ns, normalized, label='Exhaustive')
        plt.xlabel('n')
        plt.ylabel('t(n) / (n 2^n)')
        plt.title(f'Normalized Runtime - alpha={alpha}')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'exhaustive_plots_alpha_{alpha}.png')
        plt.close()

# To run and generate plots
run_big_o_validation()  