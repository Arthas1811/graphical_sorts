from typing import Callable, Optional


def is_non_decreasing(values) -> bool:
    return all(values[idx] <= values[idx + 1] for idx in range(len(values) - 1))


def binary_search(
    array,
    target,
    visualizer: Callable[[list[str]], None],
    should_stop: Optional[Callable[[], bool]] = None,
    *,
    default_color: str = "blue",
    range_color: str = "cyan",
    current_color: str = "yellow",
    visited_color: str = "gray",
    found_color: str = "green",
):
    """
    Visual binary search over a sorted array.

    Returns a tuple ``(index, colors)`` where ``index`` is:
    - found index if value exists
    - -1 if value does not exist
    - None if cancelled via ``should_stop``
    """
    low = 0
    high = len(array) - 1

    while low <= high:
        if should_stop and should_stop():
            return None, [default_color] * len(array)

        mid = (low + high) // 2
        colors = [default_color] * len(array)
        colors[low : high + 1] = [range_color] * (high - low + 1)
        colors[mid] = current_color
        visualizer(colors)

        if array[mid] == target:
            colors[mid] = found_color
            return mid, colors

        if array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, [visited_color] * len(array)
