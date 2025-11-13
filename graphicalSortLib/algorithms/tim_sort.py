def tim_sort(array, visualizer):
    RUN = 32

    def insertion_sort(arr, left, right):
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                colors = ["blue"] * len(arr)
                for x in range(left, i + 1):
                    colors[x] = "yellow"  # Bereich in Bearbeitung
                colors[j + 1] = "red"  # Bewegung
                visualizer(arr, colors)
            arr[j + 1] = key
        visualizer(arr, ["blue"] * len(arr))

    def merge(arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            colors = ["blue"] * len(arr)
            for x in range(left, right + 1):
                colors[x] = "yellow"
            colors[k] = "red"  # Einfügeposition
            visualizer(arr, colors)

            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            k += 1

        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1

        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1

        visualizer(arr, ["green" if left <= x <= right else "blue" for x in range(len(arr))])

    n = len(array)
    for i in range(0, n, RUN):
        insertion_sort(array, i, min(i + RUN - 1, n - 1))

    size = RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge(array, left, mid, right)
        size *= 2

    visualizer(array, ["green"] * n)
