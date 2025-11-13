import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def bubble_sort_visualized_with_colors(arr, doPrint=False):
    frames = []  # Speichert die Zustände der Balken
    n = len(arr)
    
    # Initiale Farben (alle Balken blau)
    current_colors = ["blue"] * n
    
    for i in range(n):
        didnothing = True
        for j in range(0, n - i - 1):
            if doPrint:
                print(f"Comparing: arr[{j}] = {arr[j]} and arr[{j+1}] = {arr[j+1]}")

            # Markiere die aktuellen Vergleiche rot
            current_colors = ["blue"] * n
            current_colors[j] = "red"
            current_colors[j + 1] = "red"
            frames.append((list(arr), list(current_colors)))
            
            # Tausche Elemente, falls notwendig
            if arr[j] > arr[j + 1]:
                if doPrint:
                    print(f"Switching: arr[{j}] = {arr[j]} and arr[{j+1}] = {arr[j+1]}")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                didnothing = False
            
            # Füge den neuen Zustand hinzu
            frames.append((list(arr), list(current_colors)))
        
        # Markiere den sortierten Bereich grün
        current_colors = ["blue"] * (n - i - 1) + ["green"] * (i + 1)
        frames.append((list(arr), list(current_colors)))
        
        if didnothing:  # Wenn kein Element getauscht wurde, ist die Liste sortiert
            if doPrint:
                print(f"No Changes {i}, Exiting.")
            break

    # Färbe die gesamte Darstellung grün, wenn die Liste sortiert ist
    final_colors = ["green"] * n
    frames.append((list(arr), final_colors))
    
    if doPrint:
        print(f"Sorted List: {arr}")
    
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
interval = 50
# Länge der zu sortierenden Liste angeben
length = 20

# Benutzerdefinierten Array eingeben, leer lassen, um ein zufälliges Array zu verwenden
array = []

# Auf True setzen, um Zwischenresultate in der Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)

frames = bubble_sort_visualized_with_colors(array, doPrint=doPrint)
animate_sort_with_colors(frames, interval)
