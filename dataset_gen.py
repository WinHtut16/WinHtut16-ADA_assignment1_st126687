import random

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

# Example usage with n=10, D=10, and seed for reproducibility
n = 10
D = 10
seed = 42  # Optional: for reproducible results

# High overlap (α=0.1)
high_overlap = generate_uniform_dataset(n, D, alpha=0.1, seed=seed)
print("High Overlap Dataset (α=0.1):")
for interval in high_overlap:
    print(interval)

# Medium overlap (α=1)
medium_overlap = generate_uniform_dataset(n, D, alpha=1, seed=seed)
print("\nMedium Overlap Dataset (α=1):")
for interval in medium_overlap:
    print(interval)

# Low overlap (α=5)
low_overlap = generate_uniform_dataset(n, D, alpha=5, seed=seed)
print("\nLow Overlap Dataset (α=5):")
for interval in low_overlap:
    print(interval)