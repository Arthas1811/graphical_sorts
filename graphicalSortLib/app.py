import math
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox



def _adaptive_delay(length, base_delay, baseline=200):
    """Drop the delay as arrays grow so the framerate is never throttled."""
    normalized_delay = max(0.0, base_delay)
    if normalized_delay == 0.0 or length <= 0:
        return 0.0
    if length <= baseline:
        return normalized_delay
    over = max(0, length - baseline)
    span = baseline if baseline > 0 else 1
    factor = max(0.0, 1 - over / span)
    return normalized_delay * factor


def _frame_skip_interval(length, base=50, visible_capacity=None, estimated_ops=None):
    """Return how many updates to skip to keep rendering responsive."""
    capacity = visible_capacity if visible_capacity and visible_capacity > 0 else base
    if capacity <= 0:
        capacity = 1
    scale_size = estimated_ops if estimated_ops and estimated_ops > 0 else length
    if scale_size <= 0:
        return 1
    if scale_size <= capacity:
        return 1
    return max(1, math.ceil(scale_size / capacity))


def _downsample(values, colors, max_samples, default_color):
    """Reduce the dataset so each rendered bar stays at least 1px wide."""
    length = len(values)
    if max_samples is None or max_samples <= 0 or length <= max_samples:
        return values, colors

    chunk = max(1, -(-length // max_samples))
    ds_values = []
    ds_colors = []
    for start in range(0, length, chunk):
        end = min(length, start + chunk)
        chunk_values = values[start:end]
        chunk_colors = colors[start:end]
        ds_values.append(max(chunk_values))
        ds_color = default_color
        for color in chunk_colors:
            if color != default_color:
                ds_color = color
                break
        ds_colors.append(ds_color)
    return ds_values, ds_colors


_N_LOG_N_ALGOS = {
    "Quick Sort",
    "Heap Sort",
    "Tim Sort",
    "Merge Sort",
}

_N_SQUARED_ALGOS = {
    "Insertion Sort",
    "Selection Sort",
    "Bubble Sort",
    "Binary Insertion Sort",
}


def _estimate_total_operations(algorithm_name, length):
    """Estimate how many visualization updates the algorithm may trigger."""
    if length <= 0:
        return 0
    n = max(1, length)
    if algorithm_name in _N_LOG_N_ALGOS:
        return n * math.log2(n)
    if algorithm_name in _N_SQUARED_ALGOS:
        return n * n
    if algorithm_name == "Bogo Sort":
        return n ** 3
    return n


DEFAULT_BAR_COLOR = "#1f77b4"

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
        self.delay = tk.DoubleVar(value=0.1)
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
            colors = [DEFAULT_BAR_COLOR] * len(self.array)

        width_px = self.canvas.winfo_width()
        width = max(width_px, 1)
        height = max(self.canvas.winfo_height(), 1)
        capacity = self._visible_capacity()
        max_visible_bars = capacity if capacity else int(width)
        max_visible_bars = max(1, max_visible_bars)
        display_values, display_colors = _downsample(self.array, colors, max_visible_bars, DEFAULT_BAR_COLOR)

        max_value = max(display_values)
        if max_value == 0:
            max_value = 1
        display_len = len(display_values)
        bar_width = width / display_len

        def bar_coords(index, value):
            x0 = index * bar_width
            x1 = x0 + bar_width
            bar_height = (value / max_value) * (height - 10)
            y0 = height - bar_height
            return x0, y0, x1, height

        if len(self.rectangles) != display_len:
            self.canvas.delete("all")
            self.rectangles = []
            for index, value in enumerate(display_values):
                coords = bar_coords(index, value)
                rect_id = self.canvas.create_rectangle(*coords, fill=display_colors[index], outline="")
                self.rectangles.append(rect_id)
        else:
            for index, value in enumerate(display_values):
                rect_id = self.rectangles[index]
                coords = bar_coords(index, value)
                self.canvas.coords(rect_id, *coords)
                self.canvas.itemconfig(rect_id, fill=display_colors[index])

        self.canvas.update_idletasks()

    def _visible_capacity(self):
        if not hasattr(self, "canvas"):
            return None
        width = self.canvas.winfo_width()
        if width <= 0:
            return None
        return max(1, int(width))

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
        selected_algo_name = self.algorithm.get()
        algorithm = algorithms[selected_algo_name]

        def run_sorting():
            frame_state = {"count": 0}
            total_ops_estimate = _estimate_total_operations(selected_algo_name, len(self.array))

            def visualizer(array, colors):
                if self.stop_sorting:
                    return
                if self.output_after_swap.get():
                    print("Current Array:", array)  # Ausgabe der Liste nach jedem Tausch
                frame_state["count"] += 1
                capacity = self._visible_capacity()
                skip_interval = _frame_skip_interval(
                    len(array),
                    visible_capacity=capacity,
                    estimated_ops=total_ops_estimate,
                )
                if frame_state["count"] % skip_interval != 0:
                    return
                self.update_plot(colors)
                self.root.update_idletasks()
                frame_delay = _adaptive_delay(len(array), self.delay.get())
                self.root.after(int(frame_delay * 1000))

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
