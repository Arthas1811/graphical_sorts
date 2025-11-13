import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class TimsortVisualizer:
    def __init__(self, doPrint=False):
        self.doPrint = doPrint

    def insertion_sort(self, arr, left, right, frames):
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1

            # Visualisiere den aktuellen Zustand
            self._add_frame(arr, frames, left, right, current=i)

            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                self._add_frame(arr, frames, left, right, current=j)

            arr[j + 1] = key
            self._add_frame(arr, frames, left, right)

            if self.doPrint:
                print(f"InsertionSort: Placed {key} at index {j + 1}, Current Array: {arr}")

    def merge(self, arr, left, mid, right, frames):
        left_subarr = arr[left:mid + 1]
        right_subarr = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        if self.doPrint:
            print(f"Merging: left {left_subarr}, right {right_subarr}")

        while i < len(left_subarr) and j < len(right_subarr):
            if left_subarr[i] <= right_subarr[j]:
                arr[k] = left_subarr[i]
                i += 1
            else:
                arr[k] = right_subarr[j]
                j += 1
            k += 1

            self._add_frame(arr, frames, left, right, mid=mid, current=k)

        while i < len(left_subarr):
            arr[k] = left_subarr[i]
            i += 1
            k += 1
            self._add_frame(arr, frames, left, right)

        while j < len(right_subarr):
            arr[k] = right_subarr[j]
            j += 1
            k += 1
            self._add_frame(arr, frames, left, right)

        self._add_frame(arr, frames, left, right, final=True)

        if self.doPrint:
            print(f"Merged Segment ({left}-{right}): {arr[left:right + 1]}")

    def timsort(self, arr, frames):
        min_run = 32
        n = len(arr)

        for start in range(0, n, min_run):
            end = min(start + min_run - 1, n - 1)
            self.insertion_sort(arr, start, end, frames)
            if self.doPrint:
                print(f"After Insertion Sort ({start}-{end}): {arr}")

        size = min_run
        while size < n:
            for start in range(0, n, 2 * size):
                mid = min(n - 1, start + size - 1)
                end = min((start + 2 * size - 1), n - 1)
                if mid < end:
                    self.merge(arr, start, mid, end, frames)
            if self.doPrint:
                print(f"After Merge Step (size={size}): {arr}")
            size *= 2

        self._add_frame(arr, frames, final=True)

        if self.doPrint:
            print(f"Final Sorted Array: {arr}")

    def _add_frame(self, arr, frames, left=None, right=None, mid=None, current=None, final=False):
        colors = ["blue"] * len(arr)
        if left is not None and right is not None:
            colors[left:right + 1] = ["yellow"] * (right - left + 1)
        if current is not None:
            colors[current] = "red"
        if final:
            colors = ["green"] * len(arr)
        frames.append((list(arr), list(colors)))


def timsort_visualized(arr, doPrint=False):
    frames = []
    sorter = TimsortVisualizer(doPrint=doPrint)
    sorter.timsort(arr, frames)
    return frames


def animate_sort_with_colors(frames, interval):
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
interval = 50
# Länge der zu Sortierenden Liste angeben
length = 50

# Benutzerdefinierten Array eingeben, leer lassen um random Array zu benutzen
array = []

# Auf True Setzen um Zwischenresultate in Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)

frames = timsort_visualized(array, doPrint=doPrint)
animate_sort_with_colors(frames, interval)
