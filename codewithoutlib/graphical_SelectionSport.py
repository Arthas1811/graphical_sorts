import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class SelectionSortVisualizer:
    def __init__(self, doPrint=False):
        self.doPrint = doPrint

    def selection_sort(self, arr, frames):
        n = len(arr)
        for i in range(n):
            min_index = i

            # Markiere den aktuellen Bereich (gelb)
            self._add_frame(arr, frames, current_range=(i, n))

            for j in range(i + 1, n):
                # Markiere das aktuelle Minimum (orange) und das überprüfte Element (rot)
                self._add_frame(arr, frames, current_min=min_index, current_check=j, current_range=(i, j + 1))

                if arr[j] < arr[min_index]:
                    min_index = j
                    if self.doPrint:
                        print(f"New minimum found at index {min_index}: {arr[min_index]}")

            # Tausche das aktuelle Element mit dem Minimum
            arr[i], arr[min_index] = arr[min_index], arr[i]

            if self.doPrint:
                print(f"Swapped elements at index {i} and {min_index}: {arr}")

            # Markiere den sortierten Bereich (grün)
            self._add_frame(arr, frames, sorted_index=i)

        # Alles grün färben, wenn die Sortierung abgeschlossen ist
        self._add_frame(arr, frames, final=True)

    def _add_frame(self, arr, frames, current_min=None, current_check=None, current_range=None, sorted_index=None, final=False):
        colors = ["blue"] * len(arr)

        if current_range:
            start, end = current_range
            colors[start:end] = ["yellow"] * (end - start)

        if current_min is not None:
            colors[current_min] = "orange"

        if current_check is not None:
            colors[current_check] = "red"

        if sorted_index is not None:
            colors[:sorted_index + 1] = ["green"] * (sorted_index + 1)

        if final:
            colors = ["green"] * len(arr)

        frames.append((list(arr), colors))


def selection_sort_visualized(arr, doPrint=False):
    # Initialisiert den Sortierprozess und speichert die Frames.
    frames = []
    sorter = SelectionSortVisualizer(doPrint=doPrint)
    sorter.selection_sort(arr, frames)
    return frames


def animate_sort_with_colors(frames, interval):
    # Erstellt die Animation basierend auf den Frames.
    fig, ax = plt.subplots()
    bar_rects = ax.bar(range(len(frames[0][0])), frames[0][0], align="center", color="blue")
    ax.set_xlim(0, len(frames[0][0]) - 1)
    ax.set_ylim(0, max(frames[0][0]) + 1)

    def update(frame):
        values, frame_colors = frame
        for rect, height, color in zip(bar_rects, values, frame_colors):
            rect.set_height(height)
            rect.set_color(color)
        return bar_rects

    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=interval, repeat=False
    )
    plt.show()


# Geschwindigkeit Festlegen (kleinerer Wert = schneller)
interval = 100
# Länge der zu sortierenden Liste angeben
length = 20

# Benutzerdefinierten Array eingeben, leer lassen um random Array zu benutzen
array = []

# Auf True Setzen, um Zwischenresultate in der Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)

frames = selection_sort_visualized(array, doPrint=doPrint)
animate_sort_with_colors(frames, interval)
