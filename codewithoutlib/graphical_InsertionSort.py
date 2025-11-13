import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def insertion_sort_visualized(arr):
    frames = []  # Speichert die Zustände der Balken
    n = len(arr)
    colors = ["blue"] * n  # Initiale Farben (alle Balken blau)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1

        # Markiere das aktuelle Element rot
        current_colors = ["green"] * i + ["red"] + ["blue"] * (n - i - 1)
        frames.append((list(arr), list(current_colors)))

        while j >= 0 and arr[j] > key:
            # Verschiebe das Element und aktualisiere die Farben
            arr[j + 1] = arr[j]
            j -= 1
            
            current_colors = ["green"] * (j + 1) + ["red"] * (i - j) + ["blue"] * (n - i - 1)
            frames.append((list(arr), list(current_colors)))
        
        arr[j + 1] = key

        # Nach Abschluss des aktuellen Schritts: Markiere den sortierten Bereich grün
        current_colors = ["green"] * (i + 1) + ["blue"] * (n - i - 1)
        frames.append((list(arr), list(current_colors)))

    # Färbe alle Balken grün, wenn die Sortierung abgeschlossen ist
    final_colors = ["green"] * n
    frames.append((list(arr), final_colors))
    
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

#Geschwindigkeit Festlegen (kleinerer Wert = schneller)
interval = 500
#Länge der zu Sortierenden Liste angeben
length = 15

#Benutzerdefinierten Array eingeben, leer lassen um random Array zu benutzen
array = []

#Auf True Setzen um Zwischenresultate in Konsole anzuzeigen
doPrint = False

if len(array) == 0:
    array = [i for i in range(length)]
    random.shuffle(array)
    
frames = insertion_sort_visualized(array)
animate_sort_with_colors(frames, interval)
