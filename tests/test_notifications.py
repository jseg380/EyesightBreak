from __future__ import annotations

import pytest

from eyesight_break.config import BreakType
from eyesight_break.notifications import send_notification


@pytest.mark.asyncio
async def test_send_notification(mocker):
    mock_notifier = mocker.MagicMock()
    await send_notification(mock_notifier, BreakType.SHORT)
    mock_notifier.send.assert_called_once()
