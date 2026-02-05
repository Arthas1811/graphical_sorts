"""
Graphical sorting visualizer package that can be imported and executed with ``graphicalSortLib.run()``.
"""

from __future__ import annotations

import os
import sys
import threading
import tkinter as _tk
from pathlib import Path
from typing import Iterable, Optional

from .app import SortingVisualizerApp

__all__ = ["run", "SortingVisualizerApp"]

_root: Optional[_tk.Tk] = None
_app: Optional[SortingVisualizerApp] = None
_lock = threading.Lock()
_tcl_configured = False


def _create_tk_root() -> _tk.Tk:
    """
    Build a Tk root, retrying once with an explicit Tcl/Tk path discovery if needed.
    """
    try:
        return _tk.Tk()
    except _tk.TclError as exc:
        if not _looks_like_missing_tcl_runtime(exc):
            raise
        _ensure_tcl_runtime(force=True)
        try:
            return _tk.Tk()
        except _tk.TclError as second_exc:
            raise RuntimeError(
                "graphicalSortLib could not locate the Tcl/Tk runtime. "
                "Reinstall Python with the 'tcl/tk and IDLE' optional feature "
                "or set the TCL_LIBRARY/TK_LIBRARY environment variables."
            ) from second_exc


def _looks_like_missing_tcl_runtime(exc: BaseException) -> bool:
    message = str(exc).lower()
    return "init.tcl" in message or "tcl wasn't installed properly" in message


def _ensure_tcl_runtime(force: bool = False) -> None:
    global _tcl_configured
    if _tcl_configured and not force:
        return
    for env_name, prefix, version_hint in (
        ("TCL_LIBRARY", "tcl", getattr(_tk, "TclVersion", 8.6)),
        ("TK_LIBRARY", "tk", getattr(_tk, "TkVersion", 8.6)),
    ):
        _configure_library_path(env_name, prefix, version_hint)
    _tcl_configured = True


def _configure_library_path(env_name: str, prefix: str, version_hint: float) -> Optional[Path]:
    current = os.environ.get(env_name)
    if _is_valid_tcl_dir(current):
        return Path(current)
    located = _find_library(prefix, version_hint)
    if located is not None:
        os.environ[env_name] = str(located)
    return located


def _is_valid_tcl_dir(path_value: Optional[os.PathLike[str] | str]) -> bool:
    if not path_value:
        return False
    return Path(path_value).joinpath("init.tcl").is_file()


def _find_library(prefix: str, version_hint: float) -> Optional[Path]:
    suffixes = _version_suffixes(version_hint)
    for parent in _library_search_dirs():
        if not parent.is_dir():
            continue
        for suffix in suffixes:
            candidate = parent / f"{prefix}{suffix}"
            if _is_valid_tcl_dir(candidate):
                return candidate
        for candidate in parent.glob(f"{prefix}*"):
            if _is_valid_tcl_dir(candidate):
                return candidate
    return None


def _version_suffixes(version_hint: float) -> list[str]:
    version_text = str(version_hint)
    parts = version_text.split(".")
    major = parts[0]
    minor = parts[1] if len(parts) > 1 else "0"
    suffixes = [
        f"{major}.{minor}",
        f"{major}{minor}",
        major,
    ]
    # Use dict.fromkeys to preserve order while removing duplicates.
    return list(dict.fromkeys(suffixes))


def _library_search_dirs() -> Iterable[Path]:
    tk_module_path = Path(_tk.__file__).resolve()
    python_root = tk_module_path.parent.parent.parent
    base_candidates: list[Path] = []
    for raw in (
        getattr(sys, "prefix", ""),
        getattr(sys, "base_prefix", ""),
        getattr(sys, "exec_prefix", ""),
        getattr(sys, "base_exec_prefix", getattr(sys, "base_prefix", "")),
    ):
        if raw:
            base_candidates.append(Path(raw))
    base_candidates.extend([python_root, python_root / "tcl"])
    expanded: list[Path] = []
    for base in _dedup_paths(base_candidates):
        expanded.extend(
            _dedup_paths(
                [
                    base,
                    base / "tcl",
                    base / "lib",
                    base / "Lib",
                    base / "Library",
                    base / "Library" / "lib",
                ]
            )
        )
    return list(_dedup_paths(expanded))


def _dedup_paths(paths: Iterable[Optional[Path]]) -> Iterable[Path]:
    seen: set[str] = set()
    for path in paths:
        if path is None:
            continue
        try:
            resolved = path.resolve()
        except OSError:
            resolved = path
        key = str(resolved).lower()
        if key in seen:
            continue
        seen.add(key)
        yield path


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

        root = _create_tk_root()
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
