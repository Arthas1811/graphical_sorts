REFERENCE_ELEMENT_COUNT = 50
MIN_DELAY = 0.002
MAX_DELAY = 0.5
DEFAULT_DELAY = 0.1


def get_adaptive_delay(base_delay: float, element_count: int) -> float:
    """Return a frame delay scaled by the current element count."""
    if element_count <= 0:
        return base_delay
    scaled_delay = base_delay * (REFERENCE_ELEMENT_COUNT / element_count)
    if scaled_delay < MIN_DELAY:
        return MIN_DELAY
    if scaled_delay > MAX_DELAY:
        return MAX_DELAY
    return scaled_delay

import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading

from algorithms.quick_sort import quick_sort
from algorithms.heap_sort import heap_sort
from algorithms.tim_sort import tim_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.selection_sort import selection_sort
from algorithms.bubble_sort import bubble_sort
from algorithms.bogo_sort import bogosort
from algorithms.binary_insertion_sort import binary_insertion_sort


class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")

        self.array = []
        self.algorithm = tk.StringVar()
        self.delay = tk.DoubleVar(value=DEFAULT_DELAY)
        self.stop_sorting = False  # Zum Stoppen der Sortierung
        self.sorting_thread = None  # Referenz für den Sortier-Thread
        self.array_mode = tk.StringVar(value="generate")  # Default: Generate Array
        self.output_after_swap = tk.BooleanVar(value=False)  # Ausgabe nach jedem Tausch
        self.rectangles = []

        self.create_widgets()
        self.setup_plot()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Radiobuttons für Array-Optionen
        tk.Radiobutton(frame, text="Generate Array", variable=self.array_mode, value="generate",
                       command=self.toggle_array_mode).grid(row=0, column=0, padx=5, sticky="w")
        tk.Radiobutton(frame, text="Use Custom Array", variable=self.array_mode, value="custom",
                       command=self.toggle_array_mode).grid(row=0, column=1, padx=5, sticky="w")

        # Array-Größe und -Generierung
        self.array_size_label = tk.Label(frame, text="Array Size:")
        self.array_size_label.grid(row=1, column=0, padx=5)
        self.array_size = tk.IntVar(value=50)
        self.array_size_entry = tk.Entry(frame, textvariable=self.array_size, width=5)
        self.array_size_entry.grid(row=1, column=1, padx=5)

        self.generate_array_button = tk.Button(frame, text="Generate Array", command=self.generate_array)
        self.generate_array_button.grid(row=1, column=2, padx=5)

        self.shuffle_array_button = tk.Button(frame, text="Shuffle Array", command=self.shuffle_array)
        self.shuffle_array_button.grid(row=1, column=3, padx=5)

        # Custom Array
        self.custom_array_label = tk.Label(frame, text="Custom Array:")
        self.custom_array = tk.StringVar()
        self.custom_array_entry = tk.Entry(frame, textvariable=self.custom_array, width=30)
        self.use_custom_array_button = tk.Button(frame, text="Use Custom Array", command=self.use_custom_array)

        # Algorithmenauswahl
        tk.Label(frame, text="Sorting Algorithm:").grid(row=2, column=0, padx=5)
        algo_menu = ttk.Combobox(frame, textvariable=self.algorithm, state="readonly", width=20)
        algo_menu["values"] = [
            "Quick Sort", "Heap Sort", "Tim Sort", "Insertion Sort",
            "Merge Sort", "Selection Sort", "Bubble Sort", "Bogo Sort", "Binary Insertion Sort",
        ]
        algo_menu.grid(row=2, column=1, padx=5)
        algo_menu.current(0)

        # Animationsverzögerung
        tk.Label(frame, text="Animation Delay (s):").grid(row=3, column=0, padx=5)
        tk.Entry(frame, textvariable=self.delay, width=5).grid(row=3, column=1, padx=5)

        # Kontrollkästchen: Ausgabe nach jedem Tausch
        self.output_checkbox = tk.Checkbutton(frame, text="Output List After Each Swap",
                                              variable=self.output_after_swap, onvalue=True, offvalue=False)
        self.output_checkbox.grid(row=4, column=0, columnspan=2, sticky="w", padx=5)

        # Steuerbuttons
        buttons = tk.Frame(self.root)
        buttons.pack(pady=10)
        tk.Button(buttons, text="Start Sorting", command=self.start_sorting).pack(side="left", padx=5)
        tk.Button(buttons, text="Stop Sorting", command=self.stop_sorting_action).pack(side="left", padx=5)

        self.toggle_array_mode()  # Initiales Umschalten

    def setup_plot(self):
        self.canvas = tk.Canvas(self.root, height=400, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda event: self.update_plot())

    def generate_array(self):
        """Erstellt einen sortierten Array."""
        self.array = list(range(1, self.array_size.get() + 1))
        self.update_plot()

    def shuffle_array(self):
        """Mischt den bestehenden Array."""
        if not self.array:
            messagebox.showinfo("No Array", "Please generate an array first.")
            return
        random.shuffle(self.array)
        self.update_plot()

    def use_custom_array(self):
        try:
            input_array = self.custom_array.get().strip().split()
            input_array = [int(x) for x in input_array]
            self.array = input_array
            self.update_plot()
        except ValueError:
            messagebox.showerror("Invalid Input", "Custom array must contain only integers separated by spaces.")

    def update_plot(self, colors=None):
        if not hasattr(self, "canvas"):
            return

        if not self.array:
            self.canvas.delete("all")
            self.rectangles = []
            return

        if colors is None or len(colors) != len(self.array):
            colors = ["#1f77b4"] * len(self.array)

        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        max_value = max(self.array)
        if max_value == 0:
            max_value = 1
        bar_width = max(width / len(self.array), 1)

        def bar_coords(index, value):
            x0 = index * bar_width
            x1 = x0 + bar_width
            bar_height = (value / max_value) * (height - 10)
            y0 = height - bar_height
            return x0, y0, x1, height

        if len(self.rectangles) != len(self.array):
            self.canvas.delete("all")
            self.rectangles = []
            for index, value in enumerate(self.array):
                coords = bar_coords(index, value)
                rect_id = self.canvas.create_rectangle(*coords, fill=colors[index], outline="")
                self.rectangles.append(rect_id)
        else:
            for index, value in enumerate(self.array):
                rect_id = self.rectangles[index]
                coords = bar_coords(index, value)
                self.canvas.coords(rect_id, *coords)
                self.canvas.itemconfig(rect_id, fill=colors[index])

        self.canvas.update_idletasks()

    def toggle_array_mode(self):
        """Schaltet zwischen den Modi 'Generate Array' und 'Use Custom Array'."""
        if self.array_mode.get() == "generate":
            # Zeige Array-Größe und -Generierung
            self.array_size_label.grid()
            self.array_size_entry.grid()
            self.generate_array_button.grid()
            self.shuffle_array_button.grid()
            # Verstecke Custom Array Widgets
            self.custom_array_label.grid_remove()
            self.custom_array_entry.grid_remove()
            self.use_custom_array_button.grid_remove()
        else:
            # Zeige Custom Array Widgets
            self.custom_array_label.grid(row=1, column=0, padx=5)
            self.custom_array_entry.grid(row=1, column=1, padx=5)
            self.use_custom_array_button.grid(row=1, column=2, padx=5)
            # Verstecke Array-Größe und -Generierung
            self.array_size_label.grid_remove()
            self.array_size_entry.grid_remove()
            self.generate_array_button.grid_remove()
            self.shuffle_array_button.grid_remove()

    def start_sorting(self):
        self.stop_sorting = False
        if self.sorting_thread and self.sorting_thread.is_alive():
            return

        algorithms = {
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort,
            "Tim Sort": tim_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Selection Sort": selection_sort,
            "Bubble Sort": bubble_sort,
            "Bogo Sort": bogosort,
            "Binary Insertion Sort": binary_insertion_sort,
        }
        algorithm = algorithms[self.algorithm.get()]

        def run_sorting():
            def visualizer(array, colors):
                if self.stop_sorting:
                    return
                if self.output_after_swap.get():
                    print("Current Array:", array)  # Ausgabe der Liste nach jedem Tausch
                self.update_plot(colors)
                self.root.update_idletasks()
                adaptive_delay = get_adaptive_delay(self.delay.get(), len(self.array))
                self.root.after(int(adaptive_delay * 1000))

            algorithm(self.array, visualizer)
            if not self.stop_sorting:
                self.update_plot(["green"] * len(self.array))
            
            print("Finished Sorting")

        self.sorting_thread = threading.Thread(target=run_sorting)
        self.sorting_thread.start()

    def stop_sorting_action(self):
        self.stop_sorting = True
        if self.sorting_thread and self.sorting_thread.is_alive():
            self.sorting_thread.join(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()
