def merge_sort(array, visualizer):
    def merge(left, mid, right):
        left_part = array[left:mid + 1]
        right_part = array[mid + 1:right + 1]

        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            colors = ["blue"] * len(array)
            for x in range(left, right + 1):
                colors[x] = "yellow"
            if left + i < len(array):
                colors[left + i] = "red"
            if mid + 1 + j < len(array):
                colors[mid + 1 + j] = "red"
            visualizer(array, colors)

            if left_part[i] <= right_part[j]:
                array[k] = left_part[i]
                i += 1
            else:
                array[k] = right_part[j]
                j += 1
            k += 1
            visualizer(array, colors)

        while i < len(left_part):
            array[k] = left_part[i]
            i += 1
            k += 1
            visualizer(array, colors)

        while j < len(right_part):
            array[k] = right_part[j]
            j += 1
            k += 1
            visualizer(array, colors)

    def merge_sort_recursive(left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(left, mid)
            merge_sort_recursive(mid + 1, right)
            merge(left, mid, right)

    merge_sort_recursive(0, len(array) - 1)
    visualizer(array, ["green"] * len(array))
