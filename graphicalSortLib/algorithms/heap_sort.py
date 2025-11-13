def heap_sort(array, visualizer):
    n = len(array)
    sorted_indices = set()  # Track der sortierten Indizes

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

        colors = ["green" if x in sorted_indices else "blue" for x in range(len(arr))]
        colors[largest] = "red"  # Bewegung
        visualizer(arr, colors)

    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i)

    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        sorted_indices.add(i)  # Markiere den Bereich als sortiert
        heapify(array, i, 0)
        colors = ["green" if x in sorted_indices else "blue" for x in range(len(array))]
        visualizer(array, colors)

    sorted_indices.add(0)  # Markiere die Wurzel am Ende als sortiert
    visualizer(array, ["green"] * len(array))
