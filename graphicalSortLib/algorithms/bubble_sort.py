def bubble_sort(array, visualizer):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            colors = ["blue"] * n
            colors[j] = "red"
            colors[j + 1] = "yellow"
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
            visualizer(array, colors)
        visualizer(array, ["green"] * (n - i - 1) + ["blue"] * (i + 1))
    visualizer(array, ["green"] * n)
