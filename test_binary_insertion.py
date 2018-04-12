

def binary_insertion_sort_lon(arr):
    ordered_values = []
    for num in arr:
        index_low = 0
        index_high = len(ordered_values) - 1
        is_added = False
        while index_low <= index_high:
            mid = int((index_low + index_high) / 2)
            if num == ordered_values[mid]:
                is_added = True
                break
            elif num > ordered_values[mid]:
                index_low = mid + 1
            else:
                index_high = mid - 1
        if not is_added:
            ordered_values.insert(index_low, num)
    return ordered_values


arr = [34,78,12,43,87,1,9,1,2,1,6,2,45,89,1,90,50]
print(binary_insertion_sort_lon(arr))