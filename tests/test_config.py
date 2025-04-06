from __future__ import annotations

from eyesight_break.config import BreakConfig, BreakType


def test_break_types():
    assert BreakType.SHORT.value == 'short'
    assert BreakType.LONG.value == 'long'


def test_break_config():
    config = BreakConfig(10, 60, True, ['test'])
    assert config.duration == 10
    assert config.postponeable
