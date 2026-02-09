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

# Example usage with a sample set of intervals
sample_intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]

# Run and print for EFT
eft_count, eft_selected = greedy_eft(sample_intervals)
print("EFT: Selected count =", eft_count)
print("EFT: Selected intervals =", eft_selected)

# Run and print for EST
est_count, est_selected = greedy_est(sample_intervals)
print("EST: Selected count =", est_count)
print("EST: Selected intervals =", est_selected)

# Run and print for SD
sd_count, sd_selected = greedy_sd(sample_intervals)
print("SD: Selected count =", sd_count)
print("SD: Selected intervals =", sd_selected)