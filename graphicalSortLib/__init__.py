"""
Graphical sorting visualizer package that can be imported and executed with ``graphicalSortLib.run()``.
"""

from __future__ import annotations

import threading
import tkinter as _tk
from typing import Optional

from .app import SortingVisualizerApp

__all__ = ["run", "SortingVisualizerApp"]

_root: Optional[_tk.Tk] = None
_app: Optional[SortingVisualizerApp] = None
_lock = threading.Lock()


def run() -> SortingVisualizerApp:
    """
    Launch the sorting visualizer GUI.

    Multiple invocations focus the existing window so user code can call run()
    repeatedly without spawning duplicate Tk roots.
    """
    global _root, _app
    app_instance: Optional[SortingVisualizerApp] = None
    with _lock:
        if _root is not None:
            try:
                _root.deiconify()
                _root.lift()
                _root.focus_force()
            except _tk.TclError:
                _root = None
                _app = None
            else:
                if _app is None:
                    raise RuntimeError("Sorting visualizer window is unavailable.")
                return _app

        root = _tk.Tk()
        _root = root
        _app = SortingVisualizerApp(root)
        app_instance = _app

    try:
        root.mainloop()
    finally:
        with _lock:
            _root = None
            _app = None

    if app_instance is None:
        raise RuntimeError("Failed to initialize SortingVisualizerApp.")
    return app_instance
