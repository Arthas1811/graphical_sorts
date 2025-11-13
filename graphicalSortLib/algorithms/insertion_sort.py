def insertion_sort(array, visualizer):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            colors = ["blue"] * len(array)
            colors[j] = "yellow"  # Vergleich
            colors[j + 1] = "red"  # Bewegung
            array[j + 1] = array[j]
            j -= 1
            visualizer(array, colors)
        array[j + 1] = key
        visualizer(array, ["green"] * (i + 1) + ["blue"] * (len(array) - i - 1))
    visualizer(array, ["green"] * len(array))
