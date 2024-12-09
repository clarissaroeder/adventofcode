def binary_search(target, array):
    left = 0
    right = len(array) - 1

    while left <= right:
        middle = (left + right) // 2

        if array[middle] == target:
            # optional early return
            print('target found')
        elif array[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
