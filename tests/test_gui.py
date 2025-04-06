from __future__ import annotations

from unittest.mock import MagicMock, call, patch

import pytest

from eyesight_break.gui import create_window


@pytest.fixture
def mock_tk():
    mock = MagicMock()
    mock.Tk.return_value = MagicMock()
    mock.Toplevel.return_value = MagicMock()
    return mock


def test_create_window(mock_tk):
    with patch('eyesight_break.gui.tkinter', mock_tk):
        mock_root = MagicMock()
        geometry = {'width': 800, 'height': 600, 'offset_x': 0, 'offset_y': 0}
        timer_gen = (str(i) for i in range(10))

        window = create_window(mock_root, geometry, 'Test', timer_gen)

        assert mock_tk.Toplevel.called

        window.attributes.assert_has_calls(
            [
                call('-alpha', 0.85),
                call('-fullscreen', True)
            ],
            any_order=True
        )
