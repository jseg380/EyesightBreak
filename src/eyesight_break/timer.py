from __future__ import annotations

from typing import Generator


def format_time(seconds: int) -> str:
    """Format time in seconds to minutes and seconds.

    Args:
        seconds (int): time in seconds

    Returns:
        (str): time formatted in MM:SS where MM is minutes and SS seconds

    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return f'{minutes:02}:{remaining_seconds:02}'


def timer(seconds: int) -> Generator:
    """Timer function to create a generator.

    Args:
        seconds (int): number of second the timer counts down to

    Returns:
        (Generator): when the timer is still up
        (None): when the timer rans out

    """
    n = seconds
    while n >= 0:
        yield format_time(n)
        n -= 1

    yield None
