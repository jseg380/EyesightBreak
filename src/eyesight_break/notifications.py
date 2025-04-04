from __future__ import annotations

from desktop_notifier import DesktopNotifier

from .config import PREV_TIME, BreakType


async def send_notification(notifier: DesktopNotifier, break_type: BreakType) -> None:
    await notifier.send(
        title='Eyesight Break',
        message=f'Ready for a {break_type.value.lower()} break in {PREV_TIME} seconds',
        timeout=5,
    )
