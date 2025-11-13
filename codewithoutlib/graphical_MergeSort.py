import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class MergeSortVisualizer:
    def __init__(self, doPrint=False):
        self.doPrint = doPrint

    def merge(self, arr, left, mid, right, frames):
        # Führt zwei sortierte Teilbereiche zusammen und visualisiert.
        n1 = mid - left + 1
        n2 = right - mid

        # Erzeuge temporäre Listen
        L = arr[left:left + n1]
        R = arr[mid + 1:mid + 1 + n2]

        if self.doPrint:
            print(f"Merging: {L} and {R}")

        i = j = 0
        k = left

        # Farben: Blau für alle, Rot für verglichene
        current_colors = ["blue"] * len(arr)

        while i < n1 and j < n2:
            # Markiere die zu vergleichenden Werte
            current_colors[k] = "red"
            frames.append((list(arr), list(current_colors)))

            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1

            if self.doPrint:
                print(f"Updated array: {arr}")

            k += 1

        # Kopiere die restlichen Elemente aus L
        while i < n1:
            current_colors[k] = "yellow"
            arr[k] = L[i]
            i += 1
            k += 1
            frames.append((list(arr), list(current_colors)))

        # Kopiere die restlichen Elemente aus R
        while j < n2:
            current_colors[k] = "yellow"
            arr[k] = R[j]
            j += 1
            k += 1
            frames.append((list(arr), list(current_colors)))

    def merge_sort(self, arr, left, right, frames):
        # Rekursiver Merge Sort mit Visualisierung.
        if left < right:
            mid = (left + right) // 2

            if self.doPrint:
                print(f"Dividing array: {arr[left:right + 1]}")

            # Visualisierung der Teilung
            current_colors = ["blue"] * len(arr)
            for i in range(left, right + 1):
                current_colors[i] = "yellow"
            frames.append((list(arr), list(current_colors)))

            # Sortiere die beiden Hälften
            self.merge_sort(arr, left, mid, frames)
            self.merge_sort(arr, mid + 1, right, frames)

            # Führe die beiden Hälften zusammen
            self.merge(arr, left, mid, right, frames)


def merge_sort_visualized(arr, doPrint=False):
    # Initialisiert den Sortierprozess und speichert die Frames.
    frames = []
    sorter = MergeSortVisualizer(doPrint=doPrint)
    sorter.merge_sort(arr, 0, len(arr) - 1, frames)

    # Färbe alles grün, wenn die Sortierung abgeschlossen ist
    final_colors = ["green"] * len(arr)
    frames.append((list(arr), final_colors))
    return frames


def animate_sort_with_colors(frames, interval):
    # Erstellt die Animation basierend auf den Frames.
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

    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=interval, repeat=False
    )
    plt.show()


# Geschwindigkeit Festlegen (kleinerer Wert = schneller)
interval = 100
# Länge der zu sortierenden Liste angeben
length = 20

# Benutzerdefinierten Array eingeben, leer lassen, um random Array zu benutzen
array = []

# Auf True setzen, um Zwischenresultate in der Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)

frames = merge_sort_visualized(array, doPrint=doPrint)
animate_sort_with_colors(frames, interval)
