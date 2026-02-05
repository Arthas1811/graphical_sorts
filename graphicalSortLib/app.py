import json
import math
import random
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk


SETTINGS_PATH = Path.home() / ".graphical_sort_lib_settings.json"

_THEME_PALETTES = {
    "dark": {
        "APP_BG": "#0F131A",
        "PANEL_BG": "#171D26",
        "PANEL_BORDER": "#2A3240",
        "CANVAS_BG": "#0B1016",
        "TEXT_COLOR": "#E6EDF3",
        "MUTED_TEXT": "#9AA7B8",
        "INPUT_BG": "#111827",
        "BUTTON_BG": "#243041",
        "BUTTON_ACTIVE_BG": "#33465E",
        "START_BUTTON_BG": "#1F5F3B",
        "START_BUTTON_ACTIVE_BG": "#2A7A4C",
        "STOP_BUTTON_BG": "#5F2531",
        "STOP_BUTTON_ACTIVE_BG": "#7A3342",
        "ACCENT_COLOR": "#3DA5FF",
        "LINK_COLOR": "#7DC4FF",
        "DEFAULT_BAR_COLOR": "#4F8FF7",
        "SORTED_BAR_COLOR": "#37D67A",
        "SEARCH_RANGE_COLOR": "#2C6CA8",
        "SEARCH_CURRENT_COLOR": "#F4C542",
        "SEARCH_VISITED_COLOR": "#5B6472",
        "WARNING_COLOR": "#FFB454",
        "ERROR_COLOR": "#FF6B6B",
    },
    "light": {
        "APP_BG": "#F3F6FB",
        "PANEL_BG": "#FFFFFF",
        "PANEL_BORDER": "#CBD5E1",
        "CANVAS_BG": "#EAF0F8",
        "TEXT_COLOR": "#1F2937",
        "MUTED_TEXT": "#4B5563",
        "INPUT_BG": "#FFFFFF",
        "BUTTON_BG": "#E2E8F0",
        "BUTTON_ACTIVE_BG": "#CBD5E1",
        "START_BUTTON_BG": "#2F855A",
        "START_BUTTON_ACTIVE_BG": "#38A169",
        "STOP_BUTTON_BG": "#C53030",
        "STOP_BUTTON_ACTIVE_BG": "#E53E3E",
        "ACCENT_COLOR": "#2563EB",
        "LINK_COLOR": "#1D4ED8",
        "DEFAULT_BAR_COLOR": "#2D6DAF",
        "SORTED_BAR_COLOR": "#2F9E44",
        "SEARCH_RANGE_COLOR": "#8CB8E8",
        "SEARCH_CURRENT_COLOR": "#E3B341",
        "SEARCH_VISITED_COLOR": "#94A3B8",
        "WARNING_COLOR": "#B7791F",
        "ERROR_COLOR": "#C53030",
    },
}


def _set_theme_colors(theme_name):
    palette = _THEME_PALETTES.get(theme_name, _THEME_PALETTES["dark"])
    globals().update(palette)


_set_theme_colors("dark")


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

_SORT_ALGORITHMS = [
    "Quick Sort",
    "Heap Sort",
    "Tim Sort",
    "Insertion Sort",
    "Merge Sort",
    "Selection Sort",
    "Bubble Sort",
    "Bogo Sort",
    "Binary Insertion Sort",
]

_SEARCH_ALGORITHMS = [
    "Linear Search",
    "Binary Search",
]


def _estimate_total_operations(algorithm_name, length):
    """Estimate how many visualization updates the sort may trigger."""
    if length <= 0:
        return 0
    n = max(1, length)
    if algorithm_name in _N_LOG_N_ALGOS:
        return n * math.log2(n)
    if algorithm_name in _N_SQUARED_ALGOS:
        return n * n
    if algorithm_name == "Bogo Sort":
        return n**3
    return n


def _estimate_search_operations(algorithm_name, length):
    if length <= 0:
        return 0
    if algorithm_name == "Linear Search":
        return length
    if algorithm_name == "Binary Search":
        return max(1, int(math.log2(max(1, length))) + 1)
    return length


if __package__:
    from .algorithms.binary_search import binary_search, is_non_decreasing
    from .algorithms.binary_insertion_sort import binary_insertion_sort
    from .algorithms.bogo_sort import bogosort
    from .algorithms.bubble_sort import bubble_sort
    from .algorithms.heap_sort import heap_sort
    from .algorithms.insertion_sort import insertion_sort
    from .algorithms.linear_search import linear_search
    from .algorithms.merge_sort import merge_sort
    from .algorithms.quick_sort import quick_sort
    from .algorithms.selection_sort import selection_sort
    from .algorithms.tim_sort import tim_sort
else:
    import os
    import sys

    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    _PROJECT_ROOT = os.path.dirname(_THIS_DIR)
    if _PROJECT_ROOT not in sys.path:
        sys.path.insert(0, _PROJECT_ROOT)

    from graphicalSortLib.algorithms.binary_search import binary_search, is_non_decreasing
    from graphicalSortLib.algorithms.binary_insertion_sort import binary_insertion_sort
    from graphicalSortLib.algorithms.bogo_sort import bogosort
    from graphicalSortLib.algorithms.bubble_sort import bubble_sort
    from graphicalSortLib.algorithms.heap_sort import heap_sort
    from graphicalSortLib.algorithms.insertion_sort import insertion_sort
    from graphicalSortLib.algorithms.linear_search import linear_search
    from graphicalSortLib.algorithms.merge_sort import merge_sort
    from graphicalSortLib.algorithms.quick_sort import quick_sort
    from graphicalSortLib.algorithms.selection_sort import selection_sort
    from graphicalSortLib.algorithms.tim_sort import tim_sort


_SORTING_ALGORITHM_MAP = {
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

_SEARCH_ALGORITHM_MAP = {
    "Linear Search": linear_search,
    "Binary Search": binary_search,
}


class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self._settings = self._load_settings()
        self.current_theme = "dark"
        self.theme_mode = tk.StringVar(value="dark")
        self._apply_theme(self._settings.get("theme", "dark"))
        self.root.configure(bg=APP_BG)
        self.root.geometry("1120x700")
        self.root.minsize(920, 580)

        self.array = []
        self.algorithm = tk.StringVar(value=_SORT_ALGORITHMS[0])
        self.visualization_mode = tk.StringVar(value="sort")
        self.array_size = tk.IntVar(value=50)
        self.custom_array = tk.StringVar()
        self.search_target = tk.StringVar()
        self.delay = tk.DoubleVar(value=0.1)
        self.stop_sorting = False
        self.sorting_thread = None
        self.array_mode = tk.StringVar(value="generate")
        self.output_after_swap = tk.BooleanVar(value=False)
        self.status_text = tk.StringVar(value="Ready")
        self.status_color = MUTED_TEXT
        self.rectangles = []

        self._configure_styles()
        self.create_widgets()
        self.setup_plot()
        self._add_signature()

    def _load_settings(self):
        default = {"theme": "dark"}
        if not SETTINGS_PATH.is_file():
            return default
        try:
            data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default
        if not isinstance(data, dict):
            return default
        theme = data.get("theme", "dark")
        if theme not in _THEME_PALETTES:
            theme = "dark"
        return {"theme": theme}

    def _save_settings(self):
        try:
            SETTINGS_PATH.write_text(json.dumps(self._settings, indent=2), encoding="utf-8")
        except OSError:
            return

    def _apply_theme(self, theme_name, persist=False):
        if theme_name not in _THEME_PALETTES:
            theme_name = "dark"
        _set_theme_colors(theme_name)
        self.current_theme = theme_name
        self.theme_mode.set(theme_name)
        if persist:
            self._settings["theme"] = theme_name
            self._save_settings()

    def _on_theme_change(self):
        requested_theme = self.theme_mode.get()
        if requested_theme == self.current_theme:
            return
        if self.sorting_thread and self.sorting_thread.is_alive():
            messagebox.showinfo("Busy", "Please stop the current visualization before changing theme.")
            self.theme_mode.set(self.current_theme)
            return
        self._apply_theme(requested_theme, persist=True)
        self._rebuild_ui()

    def _rebuild_ui(self):
        if hasattr(self, "main_frame"):
            self.main_frame.destroy()
        if hasattr(self, "signature_label"):
            self.signature_label.destroy()
        self.rectangles = []
        self.root.configure(bg=APP_BG)
        self._configure_styles()
        self.create_widgets()
        self.setup_plot()
        self._add_signature()
        self.update_plot()

    def _configure_styles(self):
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure(
            "Theme.TCombobox",
            foreground=TEXT_COLOR,
            fieldbackground=INPUT_BG,
            background=BUTTON_BG,
            arrowcolor=TEXT_COLOR,
            bordercolor=PANEL_BORDER,
            lightcolor=INPUT_BG,
            darkcolor=INPUT_BG,
            padding=(6, 4),
        )
        style.map(
            "Theme.TCombobox",
            fieldbackground=[("readonly", INPUT_BG)],
            foreground=[("readonly", TEXT_COLOR)],
            background=[("readonly", BUTTON_BG)],
            selectbackground=[("readonly", ACCENT_COLOR)],
            selectforeground=[("readonly", TEXT_COLOR)],
            arrowcolor=[("readonly", TEXT_COLOR)],
        )

        self.root.option_add("*TCombobox*Listbox*Background", INPUT_BG)
        self.root.option_add("*TCombobox*Listbox*Foreground", TEXT_COLOR)
        self.root.option_add("*TCombobox*Listbox*selectBackground", ACCENT_COLOR)
        self.root.option_add("*TCombobox*Listbox*selectForeground", TEXT_COLOR)

    def _style_entry(self, entry):
        entry.configure(
            bg=INPUT_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=PANEL_BORDER,
            highlightcolor=ACCENT_COLOR,
            bd=0,
        )

    def _make_button(self, parent, text, command, bg=None, active_bg=None, fg=None, active_fg=None):
        if bg is None:
            bg = BUTTON_BG
        if active_bg is None:
            active_bg = BUTTON_ACTIVE_BG
        if fg is None:
            fg = TEXT_COLOR
        if active_fg is None:
            active_fg = fg
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=active_fg,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            highlightthickness=0,
        )

    def _set_status(self, text, color=None):
        if color is None:
            color = MUTED_TEXT
        self.status_text.set(text)
        self.status_color = color
        if hasattr(self, "status_label"):
            self.status_label.configure(fg=color)

    def _set_status_async(self, text, color=None):
        self.root.after(0, lambda: self._set_status(text, color))

    def _add_signature(self):
        label = tk.Label(
            self.root,
            text="by Arthas1811",
            fg=LINK_COLOR,
            bg=APP_BG,
            cursor="hand2",
        )
        label.bind(
            "<Button-1>",
            lambda _event: webbrowser.open_new_tab("https://github.com/Arthas1811"),
        )
        label.place(relx=1.0, rely=1.0, anchor="se", x=-12, y=-8)
        self.signature_label = label

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=APP_BG)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        header_frame = tk.Frame(self.main_frame, bg=APP_BG)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        self.title_label = tk.Label(
            header_frame,
            text="Sorting and Searching Visualizer",
            bg=APP_BG,
            fg=TEXT_COLOR,
            font=("Segoe UI", 16, "bold"),
        )
        self.title_label.pack(anchor="w")
        self.subtitle_label = tk.Label(
            header_frame,
            text="Visualize sort and search algorithms with generated or custom arrays",
            bg=APP_BG,
            fg=MUTED_TEXT,
            font=("Segoe UI", 10),
        )
        self.subtitle_label.pack(anchor="w")

        self.controls_frame = tk.Frame(
            self.main_frame,
            bg=PANEL_BG,
            highlightthickness=1,
            highlightbackground=PANEL_BORDER,
        )
        self.controls_frame.pack(fill=tk.X, pady=(0, 10))
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_columnconfigure(2, weight=1)

        radio_style = {
            "bg": PANEL_BG,
            "fg": TEXT_COLOR,
            "activebackground": PANEL_BG,
            "activeforeground": TEXT_COLOR,
            "selectcolor": INPUT_BG,
            "highlightthickness": 0,
        }
        label_style = {"bg": PANEL_BG, "fg": MUTED_TEXT}

        mode_frame = tk.Frame(self.controls_frame, bg=PANEL_BG)
        mode_frame.grid(row=0, column=0, columnspan=8, sticky="w", padx=12, pady=(10, 4))
        tk.Radiobutton(
            mode_frame,
            text="Generate Array",
            variable=self.array_mode,
            value="generate",
            command=self.toggle_array_mode,
            **radio_style,
        ).pack(side=tk.LEFT, padx=(0, 12))
        tk.Radiobutton(
            mode_frame,
            text="Use Custom Array",
            variable=self.array_mode,
            value="custom",
            command=self.toggle_array_mode,
            **radio_style,
        ).pack(side=tk.LEFT)

        tk.Label(mode_frame, text="Task:", **label_style).pack(side=tk.LEFT, padx=(24, 6))
        tk.Radiobutton(
            mode_frame,
            text="Sort",
            variable=self.visualization_mode,
            value="sort",
            command=self.toggle_visualization_mode,
            **radio_style,
        ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Radiobutton(
            mode_frame,
            text="Search",
            variable=self.visualization_mode,
            value="search",
            command=self.toggle_visualization_mode,
            **radio_style,
        ).pack(side=tk.LEFT)

        tk.Label(mode_frame, text="Theme:", **label_style).pack(side=tk.LEFT, padx=(24, 6))
        tk.Radiobutton(
            mode_frame,
            text="Dark",
            variable=self.theme_mode,
            value="dark",
            command=self._on_theme_change,
            **radio_style,
        ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Radiobutton(
            mode_frame,
            text="Light",
            variable=self.theme_mode,
            value="light",
            command=self._on_theme_change,
            **radio_style,
        ).pack(side=tk.LEFT)

        self.array_size_label = tk.Label(self.controls_frame, text="Array Size:", **label_style)
        self.array_size_entry = tk.Entry(self.controls_frame, textvariable=self.array_size, width=8)
        self._style_entry(self.array_size_entry)
        self.generate_array_button = self._make_button(
            self.controls_frame,
            "Generate Array",
            self.generate_array,
        )
        self.generate_random_array_button = self._make_button(
            self.controls_frame,
            "Generate Random",
            self.generate_random_array,
        )
        self.shuffle_array_button = self._make_button(
            self.controls_frame,
            "Shuffle Array",
            self.shuffle_array,
        )

        self.custom_array_label = tk.Label(self.controls_frame, text="Custom Array:", **label_style)
        self.custom_array_entry = tk.Entry(self.controls_frame, textvariable=self.custom_array, width=36)
        self._style_entry(self.custom_array_entry)
        self.use_custom_array_button = self._make_button(
            self.controls_frame,
            "Apply Custom Array",
            self.use_custom_array,
        )

        self.algorithm_label = tk.Label(self.controls_frame, text="Sorting Algorithm:", **label_style)
        self.algorithm_label.grid(row=2, column=0, padx=(12, 6), pady=6, sticky="w")
        self.algo_menu = ttk.Combobox(
            self.controls_frame,
            textvariable=self.algorithm,
            state="readonly",
            width=28,
            style="Theme.TCombobox",
            values=_SORT_ALGORITHMS,
        )
        self.algo_menu.grid(row=2, column=1, padx=6, pady=6, sticky="w")
        self.algo_menu.current(0)

        self.search_target_label = tk.Label(self.controls_frame, text="Target:", **label_style)
        self.search_target_entry = tk.Entry(self.controls_frame, textvariable=self.search_target, width=12)
        self._style_entry(self.search_target_entry)

        tk.Label(self.controls_frame, text="Animation Delay (s):", **label_style).grid(
            row=3, column=0, padx=(12, 6), pady=6, sticky="w"
        )
        self.delay_entry = tk.Entry(self.controls_frame, textvariable=self.delay, width=8)
        self._style_entry(self.delay_entry)
        self.delay_entry.grid(row=3, column=1, padx=6, pady=6, sticky="w")

        self.output_checkbox = tk.Checkbutton(
            self.controls_frame,
            text="Print list after each swap",
            variable=self.output_after_swap,
            onvalue=True,
            offvalue=False,
            bg=PANEL_BG,
            fg=MUTED_TEXT,
            activebackground=PANEL_BG,
            activeforeground=TEXT_COLOR,
            selectcolor=INPUT_BG,
            highlightthickness=0,
        )
        self.output_checkbox.grid(row=3, column=2, columnspan=2, padx=6, pady=6, sticky="w")

        buttons_frame = tk.Frame(self.controls_frame, bg=PANEL_BG)
        buttons_frame.grid(row=4, column=0, columnspan=6, padx=12, pady=(4, 4), sticky="w")
        self.start_button = self._make_button(
            buttons_frame,
            "Start Sorting",
            self.start_action,
            bg=START_BUTTON_BG,
            active_bg=START_BUTTON_ACTIVE_BG,
            fg="#F8FAFC",
            active_fg="#F8FAFC",
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 8))
        self.stop_button = self._make_button(
            buttons_frame,
            "Stop",
            self.stop_sorting_action,
            bg=STOP_BUTTON_BG,
            active_bg=STOP_BUTTON_ACTIVE_BG,
            fg="#F8FAFC",
            active_fg="#F8FAFC",
        )
        self.stop_button.pack(side=tk.LEFT)

        self.status_label = tk.Label(
            self.controls_frame,
            textvariable=self.status_text,
            bg=PANEL_BG,
            fg=self.status_color,
            font=("Segoe UI", 10),
        )
        self.status_label.grid(row=5, column=0, columnspan=6, padx=12, pady=(2, 10), sticky="w")

        self.toggle_array_mode()
        self.toggle_visualization_mode()

    def setup_plot(self):
        plot_frame = tk.Frame(
            self.main_frame,
            bg=PANEL_BG,
            highlightthickness=1,
            highlightbackground=PANEL_BORDER,
        )
        plot_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(plot_frame, height=400, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.canvas.bind("<Configure>", lambda _event: self.update_plot())

    def generate_array(self):
        size = self.array_size.get()
        if size <= 0:
            messagebox.showerror("Invalid Size", "Array size must be greater than 0.")
            return
        self.array = list(range(1, size + 1))
        self.update_plot()
        self._set_status(f"Generated sorted array with {size} elements.", MUTED_TEXT)

    def generate_random_array(self):
        size = self.array_size.get()
        if size <= 0:
            messagebox.showerror("Invalid Size", "Array size must be greater than 0.")
            return
        self.array = [random.randint(1, size) for _ in range(size)]
        self.update_plot()
        self._set_status(f"Generated random array with {size} elements.", MUTED_TEXT)

    def shuffle_array(self):
        if not self.array:
            messagebox.showinfo("No Array", "Please generate or provide an array first.")
            return
        random.shuffle(self.array)
        self.update_plot()
        self._set_status("Array shuffled.", MUTED_TEXT)

    def use_custom_array(self):
        try:
            input_array = self.custom_array.get().strip().split()
            if not input_array:
                messagebox.showerror("Invalid Input", "Please enter at least one integer.")
                return
            self.array = [int(x) for x in input_array]
            self.update_plot()
            self._set_status(f"Loaded custom array with {len(self.array)} elements.", MUTED_TEXT)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Custom array must contain only integers separated by spaces.",
            )

    def update_plot(self, colors=None):
        if not hasattr(self, "canvas"):
            return

        if not self.array:
            self.canvas.delete("all")
            self.rectangles = []
            return

        if colors is None or len(colors) != len(self.array):
            colors = [DEFAULT_BAR_COLOR] * len(self.array)

        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        capacity = self._visible_capacity()
        max_visible_bars = max(1, capacity if capacity else int(width))
        display_values, display_colors = _downsample(
            self.array,
            colors,
            max_visible_bars,
            DEFAULT_BAR_COLOR,
        )

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
                rect_id = self.canvas.create_rectangle(
                    *bar_coords(index, value),
                    fill=display_colors[index],
                    outline="",
                )
                self.rectangles.append(rect_id)
        else:
            for index, value in enumerate(display_values):
                rect_id = self.rectangles[index]
                self.canvas.coords(rect_id, *bar_coords(index, value))
                self.canvas.itemconfig(rect_id, fill=display_colors[index])

        self.canvas.update_idletasks()

    def _visible_capacity(self):
        if not hasattr(self, "canvas"):
            return None
        width = self.canvas.winfo_width()
        if width <= 0:
            return None
        return max(1, int(width))

    def _draw_visual_frame(self, colors, frame_state, total_ops):
        frame_state["count"] += 1
        skip_interval = _frame_skip_interval(
            len(self.array),
            visible_capacity=self._visible_capacity(),
            estimated_ops=total_ops,
        )
        if frame_state["count"] % skip_interval != 0:
            return
        self.update_plot(colors)
        self.root.update_idletasks()
        frame_delay = _adaptive_delay(len(self.array), self.delay.get())
        self.root.after(int(frame_delay * 1000))

    def toggle_array_mode(self):
        if self.array_mode.get() == "generate":
            self.array_size_label.grid(row=1, column=0, padx=(12, 6), pady=6, sticky="w")
            self.array_size_entry.grid(row=1, column=1, padx=6, pady=6, sticky="w")
            self.generate_array_button.grid(row=1, column=2, padx=6, pady=6, sticky="w")
            self.generate_random_array_button.grid(row=1, column=3, padx=6, pady=6, sticky="w")
            self.shuffle_array_button.grid(row=1, column=4, padx=6, pady=6, sticky="w")

            self.custom_array_label.grid_remove()
            self.custom_array_entry.grid_remove()
            self.use_custom_array_button.grid_remove()
        else:
            self.custom_array_label.grid(row=1, column=0, padx=(12, 6), pady=6, sticky="w")
            self.custom_array_entry.grid(row=1, column=1, columnspan=2, padx=6, pady=6, sticky="ew")
            self.use_custom_array_button.grid(row=1, column=3, padx=6, pady=6, sticky="w")

            self.array_size_label.grid_remove()
            self.array_size_entry.grid_remove()
            self.generate_array_button.grid_remove()
            self.generate_random_array_button.grid_remove()
            self.shuffle_array_button.grid_remove()

    def toggle_visualization_mode(self):
        mode = self.visualization_mode.get()
        if mode == "sort":
            self.algorithm_label.configure(text="Sorting Algorithm:")
            self.algo_menu.configure(values=_SORT_ALGORITHMS)
            if self.algorithm.get() not in _SORT_ALGORITHMS:
                self.algorithm.set(_SORT_ALGORITHMS[0])
            self.start_button.configure(text="Start Sorting")
            self.output_checkbox.grid(row=3, column=2, columnspan=2, padx=6, pady=6, sticky="w")
            self.search_target_label.grid_remove()
            self.search_target_entry.grid_remove()
            self._set_status("Ready to sort.", MUTED_TEXT)
            return

        self.algorithm_label.configure(text="Search Algorithm:")
        self.algo_menu.configure(values=_SEARCH_ALGORITHMS)
        if self.algorithm.get() not in _SEARCH_ALGORITHMS:
            self.algorithm.set(_SEARCH_ALGORITHMS[0])
        self.start_button.configure(text="Start Search")
        self.output_checkbox.grid_remove()
        self.search_target_label.grid(row=2, column=2, padx=(12, 6), pady=6, sticky="w")
        self.search_target_entry.grid(row=2, column=3, padx=6, pady=6, sticky="w")
        self._set_status("Ready to search.", MUTED_TEXT)

    def start_action(self):
        if self.visualization_mode.get() == "search":
            self.start_search()
        else:
            self.start_sorting()

    def start_sorting(self):
        self.stop_sorting = False
        if self.sorting_thread and self.sorting_thread.is_alive():
            return
        if not self.array:
            messagebox.showinfo("No Array", "Please generate or provide an array first.")
            return

        selected_algo_name = self.algorithm.get()
        algorithm = _SORTING_ALGORITHM_MAP[selected_algo_name]
        self._set_status(f"Sorting with {selected_algo_name}...", MUTED_TEXT)

        def run_sorting():
            frame_state = {"count": 0}
            total_ops_estimate = _estimate_total_operations(selected_algo_name, len(self.array))

            def visualizer(array, colors):
                if self.stop_sorting:
                    return
                if self.output_after_swap.get():
                    print("Current Array:", array)
                self._draw_visual_frame(colors, frame_state, total_ops_estimate)

            algorithm(self.array, visualizer)
            if self.stop_sorting:
                self._set_status_async("Sorting stopped.", WARNING_COLOR)
                return

            self.update_plot([SORTED_BAR_COLOR] * len(self.array))
            self._set_status_async("Sorting finished.", SORTED_BAR_COLOR)
            print("Finished Sorting")

        self.sorting_thread = threading.Thread(target=run_sorting, daemon=True)
        self.sorting_thread.start()

    def _parse_search_target(self):
        target = self.search_target.get().strip()
        if not target:
            messagebox.showerror("Missing Target", "Please enter an integer search target.")
            return None
        try:
            return int(target)
        except ValueError:
            messagebox.showerror("Invalid Target", "Search target must be an integer.")
            return None

    def start_search(self):
        self.stop_sorting = False
        if self.sorting_thread and self.sorting_thread.is_alive():
            return
        if not self.array:
            messagebox.showinfo("No Array", "Please generate or provide an array first.")
            return

        target = self._parse_search_target()
        if target is None:
            return

        selected_search_name = self.algorithm.get()
        if selected_search_name == "Binary Search" and not is_non_decreasing(self.array):
            messagebox.showwarning(
                "Binary Search Requires Sorted Array",
                "Binary search only works on a sorted list. Sort the array first or use linear search.",
            )
            self._set_status("Binary search aborted: array is not sorted.", WARNING_COLOR)
            return

        self._set_status(f"Searching for {target} with {selected_search_name}...", MUTED_TEXT)
        search_algorithm = _SEARCH_ALGORITHM_MAP[selected_search_name]

        def run_search():
            frame_state = {"count": 0}
            total_ops = _estimate_search_operations(selected_search_name, len(self.array))

            def visualizer(colors):
                self._draw_visual_frame(colors, frame_state, total_ops)

            search_kwargs = {
                "default_color": DEFAULT_BAR_COLOR,
                "current_color": SEARCH_CURRENT_COLOR,
                "visited_color": SEARCH_VISITED_COLOR,
                "found_color": SORTED_BAR_COLOR,
            }
            if selected_search_name == "Binary Search":
                search_kwargs["range_color"] = SEARCH_RANGE_COLOR

            result_idx, final_colors = search_algorithm(
                self.array,
                target,
                visualizer,
                should_stop=lambda: self.stop_sorting,
                **search_kwargs,
            )

            self.update_plot(final_colors)

            if result_idx is None:
                self._set_status_async("Search stopped.", WARNING_COLOR)
                return

            if result_idx >= 0:
                self._set_status_async(f"Found {target} at index {result_idx}.", SORTED_BAR_COLOR)
            else:
                self._set_status_async(f"{target} not found.", ERROR_COLOR)

        self.sorting_thread = threading.Thread(target=run_search, daemon=True)
        self.sorting_thread.start()

    def stop_sorting_action(self):
        self.stop_sorting = True
        if self.sorting_thread and self.sorting_thread.is_alive():
            self._set_status("Stopping...", WARNING_COLOR)
            self.sorting_thread.join(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()
