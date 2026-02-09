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

# Example usage with a sample set of intervals
sample_intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]

# Run and print for Exhaustive
exhaustive_count, exhaustive_selected = exhaustive_interval_scheduling(sample_intervals)
print("Exhaustive: Maximum count =", exhaustive_count)
print("Exhaustive: Selected intervals =", exhaustive_selected)