def quick_sort(array, visualizer):
    sorted_indices = set()  # Speichert alle fertig sortierten Indizes

    def partition(low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
            # Farben aktualisieren
            colors = ["green" if idx in sorted_indices else "blue" for idx in range(len(array))]
            colors[high] = "yellow"  # Pivot-Element
            colors[j] = "red"  # Vergleichsindex
            colors[i] = "yellow"  # Bereich in Bearbeitung
            visualizer(array, colors)
        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pivot_index = partition(low, high)
            # Markiere das Pivot-Element als sortiert
            sorted_indices.add(pivot_index)
            # Sortiere die Teilbereiche
            quick_sort_recursive(low, pivot_index - 1)
            quick_sort_recursive(pivot_index + 1, high)
            # Nach der Rekursion: Linken und rechten Teilbereich als sortiert markieren
            sorted_indices.update(range(low, high + 1))

            colors = ["green" if idx in sorted_indices else "blue" for idx in range(len(array))]
            visualizer(array, colors)

    quick_sort_recursive(0, len(array) - 1)
    visualizer(array, ["green"] * len(array))  # Endzustand grün
