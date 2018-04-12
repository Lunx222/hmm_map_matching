import numpy as np
from util.SortAndInsert import quick_sort


def __is_all_visited(visited_arr):
    is_all_visited = True
    for mark in visited_arr:
        if mark == 0:
            is_all_visited = False
            break
    return is_all_visited


def __find_max_index_unvisited(size_arr, mark_arr):
    max_index = None
    for i in range(len(mark_arr)):
        if mark_arr[i] == 0:
            max_index = i
            break
    if max_index is None:
        return None
    for i in range(len(size_arr)):
        if (size_arr[i] > size_arr[max_index]) & \
                (mark_arr[i] == 0):
            max_index = i
    return max_index

def __HPS(size_arr, maximum_size):

    segment_index = np.zeros(len(size_arr) + 1)  # 分段坐标， 多1 表示最后一块的分割
    visited_arr = np.zeros(len(size_arr))

    current_index = __find_max_index_unvisited(size_arr, visited_arr)
    lower_seg_index = current_index - 1
    higher_seg_index = current_index + 1
    visited_arr[current_index] = 1

    estimated_state_size = size_arr[current_index]
    while current_index is not None:
        lower_size = np.math.inf
        higher_size = np.math.inf
        # 往左扫描
        if lower_seg_index >= 0:
            if visited_arr[lower_seg_index] == 0:
                # 左边走得通
                lower_size = size_arr[lower_seg_index]
        if higher_seg_index < len(size_arr):
            if visited_arr[higher_seg_index] == 0:
                # 右边走得通
                higher_size = size_arr[higher_seg_index]
        if (lower_size == np.math.inf) & (higher_size == np.math.inf):
            segment_index[lower_seg_index + 1] = 1
            segment_index[higher_seg_index] = 1
            current_index = __find_max_index_unvisited(size_arr, visited_arr)
            if current_index is not None:
                lower_seg_index = current_index - 1
                higher_seg_index = current_index + 1
                estimated_state_size = size_arr[current_index]
                visited_arr[current_index] = 1
            continue
        if lower_size < higher_size:
            estimated_state_size += lower_size
            added = 'low'
        else:
            estimated_state_size += higher_size
            added = 'high'
        if estimated_state_size <= maximum_size:
            if added == 'low':
                visited_arr[lower_seg_index] = 1
                lower_seg_index -= 1
            else:
                visited_arr[higher_seg_index] = 1
                higher_seg_index += 1
        else:
            segment_index[lower_seg_index + 1] = 1
            segment_index[higher_seg_index] = 1
            current_index = __find_max_index_unvisited(size_arr, visited_arr)
            if current_index is not None:
                lower_seg_index = current_index - 1
                higher_seg_index = current_index + 1
                visited_arr[current_index] = 1
                estimated_state_size = size_arr[current_index]

    seg_length_arr = []
    one_index_set = []
    for i in range(len(segment_index)):
        if segment_index[i] == 1:
            one_index_set.append(i)
    one_index_set.reverse()
    for j in range(len(one_index_set) - 1):
        seg_length_arr.append(one_index_set[j] - one_index_set[j + 1])
    seg_length_arr.reverse()

    offset = 0
    for k in range(len(seg_length_arr)):
        if seg_length_arr[k] < 2:
            # 太短的合并到较短的段里
            if (k - 1 >= 0) & (k + 1 < len(seg_length_arr)):
                if seg_length_arr[k - 1] < seg_length_arr[k + 1]:
                    segment_index[offset] = 0
                else:
                    segment_index[offset + 1] = 0
            else:
                if k - 1 >= 0:
                    segment_index[offset] = 9
                else:
                    segment_index[offset + 1] = 0
        offset += seg_length_arr[k]

    one_index_set = []
    for i in range(len(segment_index)):
        if segment_index[i] == 1:
            one_index_set.append(i)

    return one_index_set


sub_matched_sets = []
sub_trajs_corresponding_to_sub_matched_sets = []

size_of_candidate_set_arr = [1,2,1,3,5,8,6,4,2,3,7,1,0,9,10,2,4,5,1,6,2,7,4,4,4,9,10,20,22]
segment_index = np.zeros(len(size_of_candidate_set_arr) + 1)  # 分段坐标， 多1 表示最后一块的分割
visited_arr = np.zeros(len(size_of_candidate_set_arr))

current_index = __find_max_index_unvisited(size_of_candidate_set_arr, visited_arr)
lower_seg_index = current_index - 1
higher_seg_index = current_index + 1
visited_arr[current_index] = 1

estimated_state_size = size_of_candidate_set_arr[current_index]
while current_index is not None:
    lower_size = np.math.inf
    higher_size = np.math.inf
    # 往左扫描
    if lower_seg_index >= 0:
        if visited_arr[lower_seg_index] == 0:
            # 左边走得通
            lower_size = size_of_candidate_set_arr[lower_seg_index]
    if higher_seg_index < len(size_of_candidate_set_arr):
        if visited_arr[higher_seg_index] == 0:
            # 右边走得通
            higher_size = size_of_candidate_set_arr[higher_seg_index]
    if (lower_size == np.math.inf) & (higher_size == np.math.inf):
        segment_index[lower_seg_index + 1] = 1
        segment_index[higher_seg_index] = 1
        current_index = __find_max_index_unvisited(size_of_candidate_set_arr, visited_arr)
        if current_index is not None:
            lower_seg_index = current_index - 1
            higher_seg_index = current_index + 1
            estimated_state_size = size_of_candidate_set_arr[current_index]
            visited_arr[current_index] = 1
        continue
    if lower_size < higher_size:
        estimated_state_size += lower_size
        added = 'low'
    else:
        estimated_state_size += higher_size
        added = 'high'
    if estimated_state_size <= 20:
        if added == 'low':
            visited_arr[lower_seg_index] = 1
            lower_seg_index -= 1
        else:
            visited_arr[higher_seg_index] = 1
            higher_seg_index += 1
    else:
        segment_index[lower_seg_index + 1] = 1
        segment_index[higher_seg_index] = 1
        current_index = __find_max_index_unvisited(size_of_candidate_set_arr, visited_arr)
        if current_index is not None:
            lower_seg_index = current_index - 1
            higher_seg_index = current_index + 1
            visited_arr[current_index] = 1
            estimated_state_size = size_of_candidate_set_arr[current_index]

seg_length_arr = []
one_index_set = []
for i in range(len(segment_index)):
    if segment_index[i] == 1:
        one_index_set.append(i)
one_index_set.reverse()
for j in range(len(one_index_set)-1):
    seg_length_arr.append(one_index_set[j] - one_index_set[j+1])
seg_length_arr.reverse()

print('第一次分割：')
arr = []
for i in range(len(segment_index)-1):
    if segment_index[i] == 1:
        print(arr)
        arr.clear()
    arr.append(size_of_candidate_set_arr[i])
print(arr)
print(segment_index)
print(seg_length_arr)


offset = 0
for k in range(len(seg_length_arr)):
    if seg_length_arr[k] < 2:
        # 太短的合并到较短的段里
        if (k-1 >= 0) & (k+1 < len(seg_length_arr)):
            if seg_length_arr[k-1] < seg_length_arr[k+1]:
                segment_index[offset] = 0
            else:
                segment_index[offset+1] = 0
        else:
            if k-1 >= 0:
                segment_index[offset] = 0
            else:
                segment_index[offset+1] = 0
    offset += seg_length_arr[k]

seg_length_arr = []
one_index_set = []
for i in range(len(segment_index)):
    if segment_index[i] == 1:
        one_index_set.append(i)
one_index_set.reverse()
for j in range(len(one_index_set)-1):
    seg_length_arr.append(one_index_set[j] - one_index_set[j+1])
seg_length_arr.reverse()


print('合并处理后：')
arr = []
for i in range(len(segment_index)-1):
    if segment_index[i] == 1:
        print(arr)
        arr.clear()
    arr.append(size_of_candidate_set_arr[i])

print(arr)
print(segment_index)
print(seg_length_arr)

print("调用HPS")
print(__HPS(size_of_candidate_set_arr,20))


