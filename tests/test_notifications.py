from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from eyesight_break.config import BreakType
from eyesight_break.notifications import send_notification


@pytest.mark.asyncio
async def test_send_notification(mocker):
    # Create an async mock instead of a regular MagicMock
    mock_notifier = mocker.MagicMock()
    mock_notifier.send = AsyncMock()  # Make the send method awaitable
    
    await send_notification(mock_notifier, BreakType.SHORT)
    
    # Use assert_awaited instead of assert_called for async functions
    mock_notifier.send.assert_awaited_once()
