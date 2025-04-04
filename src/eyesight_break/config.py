from __future__ import annotations

from enum import Enum
from pathlib import Path


class BreakType(Enum):
    SHORT = 'short'
    LONG = 'long'


class BreakConfig:
    __slots__ = ('duration', 'interval', 'postponeable', 'messages')

    def __init__(self, duration: int, interval: int, postponeable: bool, messages: list[str]) -> None:
        self.duration: int = duration
        self.interval: int = interval
        self.postponeable: bool = postponeable
        self.messages: list[str] = messages


class WinConfig:
    alpha: float = 0.85
    bg_color: str = 'black'
    fg_color: str = 'white'
    title: str = 'EyesightBreak'
    font: tuple = ('Arial', 24)


INTERVAL_UNIT: int = 60 * 10
'''Time interval in seconds between breaks'''

SHORTS_INTERVALS_PER_LONG: int = 3
'''Amount of short breaks (+1) that are between two long breaks'''

PREV_TIME: int = 7
'''Time in seconds before the break begins when a notification about the upcoming break is sent'''

ICON_PATH: Path = Path('eye.svg').resolve()
'''Path of the icon of the app to show in the warning notification'''


# BreakConfig class created to avoid making spelling mistakes and not realizing
# thanks of the autocompletion help of the IDE
BREAKS: dict[BreakType, BreakConfig] = {
    BreakType.SHORT: BreakConfig(
        duration=20,
        interval=INTERVAL_UNIT,
        postponeable=False,
        messages=[
            'Tightly close your eyes',
            'Roll your eyes a few times to each side',
            'Rotate your eyes in clockwise direction',
            'Rotate your eyes in counterclockwise direction',
            'Blink your eyes',
            'Focus on a point in the far distance',
            'Have some water',
        ],
    ),
    BreakType.LONG: BreakConfig(
        duration=180,
        interval=INTERVAL_UNIT * SHORTS_INTERVALS_PER_LONG,
        postponeable=True,
        messages=[
            'Walk for a while',
            'Lean back at your seat and relax',
        ],
    ),
}
'''Dictionary containing every break with their associated configuration'''
