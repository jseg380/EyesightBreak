from __future__ import annotations

from eyesight_break.timer import format_time, timer


def test_format_time():
    assert format_time(65) == '01:05'
    assert format_time(0) == '00:00'
    assert format_time(3599) == '59:59'
    assert format_time(3600) == '60:00'


def test_timer_generator():
    gen = timer(2)
    assert next(gen) == '00:02'
    assert next(gen) == '00:01'
    assert next(gen) == '00:00'
    assert next(gen) is None
