import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class HeapSortVisualizer:
    def __init__(self, doPrint=False):
        self.doPrint = doPrint

    def heapify(self, arr, n, i, frames):
        largest = i  # Initialisiere die Wurzel als größtes Element
        left = 2 * i + 1  # Linkes Kind
        right = 2 * i + 2  # Rechtes Kind

        if self.doPrint:
            print(f"Heapifying at index {i}, left: {left}, right: {right}, array: {arr}")

        # Markiere die aktuellen Vergleichselemente
        current_colors = ["blue"] * len(arr)
        if left < n:
            current_colors[left] = "yellow"
        if right < n:
            current_colors[right] = "yellow"
        current_colors[i] = "red"  # Wurzel, die gerade bearbeitet wird
        frames.append((list(arr), list(current_colors)))

        # Vergleiche die Wurzel mit dem linken Kind
        if left < n and arr[left] > arr[largest]:
            largest = left

        # Vergleiche die Wurzel mit dem rechten Kind
        if right < n and arr[right] > arr[largest]:
            largest = right

        # Tausche die Wurzel mit dem größten Element, falls nötig
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]

            if self.doPrint:
                print(f"Swapped {arr[i]} and {arr[largest]}, updated array: {arr}")

            # Visualisiere den Swap
            current_colors = ["blue"] * len(arr)
            current_colors[i] = "green"
            current_colors[largest] = "green"
            frames.append((list(arr), list(current_colors)))

            # Rekursive Heapify-Aufrufe
            self.heapify(arr, n, largest, frames)

    def heap_sort(self, arr):
        frames = []  # Speichert die Frames für die Animation
        n = len(arr)

        if self.doPrint:
            print(f"Original array: {arr}")

        # Baue einen Max-Heap
        for i in range(n // 2 - 1, -1, -1):
            if self.doPrint:
                print(f"Building max-heap at index {i}")
            self.heapify(arr, n, i, frames)

        # Extrahiere die Elemente aus dem Heap
        for i in range(n - 1, 0, -1):
            # Tausche das Wurzelelement mit dem letzten Element
            arr[0], arr[i] = arr[i], arr[0]

            if self.doPrint:
                print(f"Extracted max element, updated array: {arr}")

            # Markiere den sortierten Bereich in Grün
            current_colors = ["blue"] * len(arr)
            current_colors[i:] = ["green"] * (n - i)
            frames.append((list(arr), list(current_colors)))

            # Heapify das reduzierte Heap
            self.heapify(arr, i, 0, frames)

        # Alles grün färben, wenn die Sortierung abgeschlossen ist
        final_colors = ["green"] * len(arr)
        frames.append((list(arr), final_colors))
        return frames


def heap_sort_visualized(arr, doPrint=False):
    sorter = HeapSortVisualizer(doPrint=doPrint)
    frames = sorter.heap_sort(arr)
    return frames


def animate_sort_with_colors(frames, interval):
    fig, ax = plt.subplots()
    bar_rects = ax.bar(range(len(frames[0][0])), frames[0][0], align="center", color="blue")
    ax.set_xlim(0, len(frames[0][0]))
    ax.set_ylim(0, max(frames[0][0]) + 1)

    def update(frame):
        values, frame_colors = frame
        for rect, height, color in zip(bar_rects, values, frame_colors):
            rect.set_height(height)
            rect.set_color(color)
        return bar_rects

    # Schnelle Animation durch Anpassung des Intervalls
    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=interval, repeat=False
    )
    plt.show()


# Geschwindigkeit Festlegen (kleinerer Wert = schneller)
interval = 10
# Länge der zu sortierenden Liste angeben
length = 20

# Benutzerdefinierten Array eingeben, leer lassen, um ein zufälliges Array zu generieren
array = []

# Auf True setzen, um Zwischenresultate in der Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)

frames = heap_sort_visualized(array, doPrint=doPrint)
animate_sort_with_colors(frames, interval)
