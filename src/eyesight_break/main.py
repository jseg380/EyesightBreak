from __future__ import annotations

from asyncio import run as async_run
from time import sleep

from desktop_notifier import DesktopNotifier, Icon

from .config import ICON_PATH, INTERVAL_UNIT, PREV_TIME, SHORTS_INTERVALS_PER_LONG, BreakType
from .gui import show_break
from .notifications import send_notification


def main():
    APP_ICON = Icon(ICON_PATH)

    notifier = DesktopNotifier(app_name='EyesightBreak', app_icon=APP_ICON)
    break_counter = 0

    while True:
        # Logic to decide which type of break should be displayed
        break_type: BreakType = BreakType.SHORT
        if break_counter % SHORTS_INTERVALS_PER_LONG and break_counter != 0:
            break_type = BreakType.LONG

        # Sleep interval between breaks
        sleep(INTERVAL_UNIT - PREV_TIME)

        # Send notification and sleep the remaining time
        async_run(send_notification(notifier, break_type))
        sleep(PREV_TIME)

        # Display break for a period of time, then redo this process again
        postponed = show_break(break_type)

        # If the break hasn't been postponed, increase the break counter
        if not postponed:
            break_counter += 1


if __name__ == '__main__':
    main()
