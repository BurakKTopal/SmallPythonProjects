import time

def binarySearch(list_search, key, left, right):
    mid = left + (right - left) // 2
    if mid == left:
        return -1
    if list_search[mid] == key:
        return mid
    elif list_search[mid] < key:
        left = mid
    else:
        right = mid
    return binarySearch(list_search, key, left, right)


test_list = [1, 4, 5, 8, 10, 15, 20, 25, 27, 28, 55, 60, 65, 66, 67, 68, 69, 70]
key = 67

timeStart1 = time.perf_counter()
result = binarySearch(test_list, key, 0, len(test_list))
timeEnd1 = time.perf_counter()
print(result)

timeStart2 = time.perf_counter()
result = key in test_list
timeEnd2 = time.perf_counter()

print(f'The binary search algorithm gave {timeEnd1 - timeStart1}')
print(f'The search function of python gave {timeEnd2 - timeStart2}')
