from typing import Callable, Optional


def linear_search(
    array,
    target,
    visualizer: Callable[[list[str]], None],
    should_stop: Optional[Callable[[], bool]] = None,
    *,
    default_color: str = "blue",
    current_color: str = "yellow",
    visited_color: str = "gray",
    found_color: str = "green",
):
    """
    Visual linear search.

    Returns a tuple ``(index, colors)`` where ``index`` is:
    - found index if value exists
    - -1 if value does not exist
    - None if cancelled via ``should_stop``
    """
    colors = [default_color] * len(array)

    for idx, value in enumerate(array):
        if should_stop and should_stop():
            return None, colors

        if idx > 0 and colors[idx - 1] != found_color:
            colors[idx - 1] = visited_color
        colors[idx] = current_color
        visualizer(colors)

        if value == target:
            colors[idx] = found_color
            return idx, colors

        colors[idx] = visited_color

    return -1, colors
