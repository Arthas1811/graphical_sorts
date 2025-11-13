def selection_sort(array, visualizer):
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            colors = ["blue"] * len(array)
            colors[min_idx] = "yellow"
            colors[j] = "red"
            if array[j] < array[min_idx]:
                min_idx = j
            visualizer(array, colors)
        array[i], array[min_idx] = array[min_idx], array[i]
        visualizer(array, ["green"] * (i + 1) + ["blue"] * (len(array) - i - 1))
    visualizer(array, ["green"] * len(array))
