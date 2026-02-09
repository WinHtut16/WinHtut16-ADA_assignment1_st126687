def interval_scheduling(intervals):
    if not intervals:
        return []
    
    # Sort intervals by finish time
    intervals.sort(key=lambda x: x[1])
    
    selected = [intervals[0]]
    last_finish = intervals[0][1]
    
    for start, finish in intervals[1:]:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish
    
    return selected

# Example usage
intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
result = interval_scheduling(intervals)
print(f"Selected intervals: {result}")
print(f"Maximum size: {len(result)}")