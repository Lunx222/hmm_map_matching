from util.GeoHelper import Coordinate


def quick_sort_lon_recursive(arr, low, high):
    if low >= high:
        return
    low_indicator = low
    high_indicator = high
    axis = low_indicator
    while high_indicator >= low_indicator:
        if arr[axis].longitude > arr[high_indicator].longitude:
            temp = arr[axis]
            arr[axis] = arr[high_indicator]
            arr[high_indicator] = temp
            axis = high_indicator
            high_indicator -= 1
            while low_indicator <= high_indicator:
                if arr[axis].longitude < arr[low_indicator].longitude:
                    temp = arr[axis]
                    arr[axis] = arr[low_indicator]
                    arr[low_indicator] = temp
                    axis = low_indicator
                    low_indicator += 1
                    break
                else:
                    low_indicator += 1
        else:
            high_indicator -= 1
    quick_sort_lon_recursive(arr, low, axis - 1)
    quick_sort_lon_recursive(arr, axis + 1, high)


coord_arr = [Coordinate(1,33),Coordinate(4,83),Coordinate(2,23),Coordinate(9,1),Coordinate(5,6)]
print(coord_arr)
quick_sort_lon_recursive(coord_arr, 0, len(coord_arr)-1)
print(coord_arr)