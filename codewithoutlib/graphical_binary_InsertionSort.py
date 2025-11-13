import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class BinaryInsertionSort:
    def __init__(self, doPrint=False):
        self.doPrint = doPrint

    def binary_search(self, arr, key, start, end, frames):
        # Visualisiere die binäre Suche
        while start < end:
            mid = (start + end) // 2
            if self.doPrint:
                print(f"Binary Search: key={key}, start={start}, end={end}, mid={mid}, arr[mid]={arr[mid]}")
            
            # Markiere den Vergleichsbereich in Gelb
            current_colors = ["blue"] * len(arr)
            current_colors[start:end + 1] = ["yellow"] * (end - start + 1)  # Visualisiert den Suchbereich
            frames.append((list(arr), list(current_colors)))
            
            if arr[mid] > key:
                end = mid
            else:
                start = mid + 1
        return start

def binary_insertion_sort_visualized(arr, doPrint=False):
    frames = []  # Speichert die Zustände der Balken
    n = len(arr)
    colors = ["blue"] * n  # Initiale Farben (alle Balken blau)
    
    bis = BinaryInsertionSort(doPrint)
    
    for i in range(1, n):
        key = arr[i]
        if doPrint:
            print(f"\Insertion of arr[{i}] = {key} into the Sorted area: {arr[:i]}")
        
        # Visualisiere den aktuellen Zustand mit rotem Schlüssel
        current_colors = ["blue"] * n
        current_colors[i] = "red"  # Zeigt das aktuell eingeordnete Element
        frames.append((list(arr), list(current_colors)))
        
        # Führe binäre Suche durch und markiere die verglichenen Bereiche in Gelb
        position = bis.binary_search(arr, key, 0, i, frames)
        
        if doPrint:
            print(f"Found Position for {key}: {position}")
        
        # Verschiebe die Elemente nach rechts
        for j in range(i, position, -1):
            arr[j] = arr[j - 1]
        
        arr[position] = key
        
        if doPrint:
            print(f"Array after inserting of {key}: {arr}")
        
        # Markiere den sortierten Bereich grün
        current_colors = ["green"] * (i + 1) + ["blue"] * (n - i - 1)
        frames.append((list(arr), list(current_colors)))

    # Färbe alle Balken grün, wenn die Sortierung abgeschlossen ist
    final_colors = ["green"] * n
    frames.append((list(arr), final_colors))
    
    if doPrint:
        print(f"\Sorted Array: {arr}")
    
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

    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=interval, repeat=False
    )
    plt.show()

# Geschwindigkeit Festlegen (kleinerer Wert = schneller)
interval = 100
# Länge der zu sortierenden Liste angeben
length = 20

# Benutzerdefinierten Array eingeben, leer lassen, um ein zufälliges Array zu verwenden
array = []

# Auf True setzen, um Zwischenresultate in der Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)

frames = binary_insertion_sort_visualized(array, doPrint=doPrint)
animate_sort_with_colors(frames, interval)
