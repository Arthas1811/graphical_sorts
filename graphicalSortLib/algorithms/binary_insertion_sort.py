def binary_insertion_sort(array, visualizer):
    def binary_search(arr, val, start, end, visualizer):
        while start < end:
            # Visualisiere den Bereich, der untersucht wird
            colors = ["green" if i < start else "yellow" if start <= i < end else "blue" for i in range(len(arr))]
            visualizer(arr, colors)

            mid = (start + end) // 2
            # Visualisiere das Element, das gerade geprüft wird
            colors[mid] = "red"
            visualizer(arr, colors)

            if arr[mid] < val:
                start = mid + 1
            else:
                end = mid

        return start

    n = len(array)
    for i in range(1, n):
        # Visualisiere den aktuellen Zustand des Arrays
        colors = ["green" if j < i else "blue" for j in range(n)]
        colors[i] = "red"  # Das aktuelle Element zum Einfügen
        visualizer(array, colors)

        val = array[i]
        # Finde die Position des aktuellen Elements mit Binary Search und visualisiere
        pos = binary_search(array, val, 0, i, visualizer)

        # Schiebe Elemente, um Platz zu schaffen
        for j in range(i, pos, -1):
            array[j] = array[j - 1]

        array[pos] = val

        # Visualisiere den Zustand nach dem Einfügen
        colors = ["green" if j <= i else "blue" for j in range(n)]
        visualizer(array, colors)

    # Markiere das gesamte Array als sortiert
    visualizer(array, ["green"] * n)
