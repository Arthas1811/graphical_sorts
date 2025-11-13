import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class QuickSortVisualizer:
    def __init__(self, doPrint=False):
        self.doPrint = doPrint

    def partition(self, low, high, arr, frames):
        pivot = arr[high]
        i = low - 1

        # Markiere den Pivot in Rot
        self._add_frame(arr, frames, pivot_index=high)

        for j in range(low, high):
            # Markiere die beiden verglichenen Elemente
            self._add_frame(arr, frames, pivot_index=high, current_check=j, swap_index=i + 1 if i >= low else None)

            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if self.doPrint:
                    print(f"Swapped elements at indices {i} and {j}: {arr}")
                # Visualisiere den Tausch
                self._add_frame(arr, frames, pivot_index=high, swap_indices=(i, j))

        # Tausche Pivot an die richtige Position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if self.doPrint:
            print(f"Placed pivot {arr[i + 1]} at position {i + 1}: {arr}")
        self._add_frame(arr, frames, pivot_index=high, swap_indices=(i + 1, high), final_pivot=i + 1)

        return i + 1

    def quick_sort(self, low, high, arr, frames):
        if low < high:
            pi = self.partition(low, high, arr, frames)

            # Sortiere den linken Bereich
            self.quick_sort(low, pi - 1, arr, frames)

            # Sortiere den rechten Bereich
            self.quick_sort(pi + 1, high, arr, frames)

    def _add_frame(self, arr, frames, pivot_index=None, current_check=None, swap_index=None, swap_indices=None, final_pivot=None):
        colors = ["blue"] * len(arr)

        if pivot_index is not None:
            colors[pivot_index] = "red"

        if current_check is not None:
            colors[current_check] = "yellow"

        if swap_index is not None:
            colors[swap_index] = "yellow"

        if swap_indices is not None:
            i, j = swap_indices
            colors[i] = "green"
            colors[j] = "green"

        if final_pivot is not None:
            colors[final_pivot] = "green"

        frames.append((list(arr), colors))


def quick_sort_visualized(arr, doPrint=False):
    # Initialisiert den Sortierprozess und speichert die Frames.
    frames = []
    sorter = QuickSortVisualizer(doPrint=doPrint)
    sorter.quick_sort(0, len(arr) - 1, arr, frames)

    # Alles grün färben, wenn die Sortierung abgeschlossen ist
    final_colors = ["green"] * len(arr)
    frames.append((list(arr), final_colors))
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
length = 30

# Benutzerdefinierten Array eingeben, leer lassen um random Array zu benutzen
array = []

# Auf True Setzen, um Zwischenresultate in der Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)

frames = quick_sort_visualized(array, doPrint=doPrint)
animate_sort_with_colors(frames, interval)
