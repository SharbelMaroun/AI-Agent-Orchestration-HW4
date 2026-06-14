"""TDD tests for the sliding-window rate limiters (tasks 9.015, 9.017, 9.019)."""

from archlens.gatekeeper.rate_config import load_rate_config, service_limits
from archlens.gatekeeper.windows import hour_window, minute_window


def _limits():
    return service_limits(load_rate_config())


def test_minute_window_admits_30_defers_31(fake_clock):
    window = minute_window(_limits(), fake_clock)
    assert all(window.allow() for _ in range(30))
    assert window.allow() is False


def test_minute_window_count_tracks_admitted(fake_clock):
    window = minute_window(_limits(), fake_clock)
    for _ in range(5):
        window.allow()
    assert window.count() == 5


def test_hour_window_admits_500_defers_501(fake_clock):
    window = hour_window(_limits(), fake_clock)
    assert all(window.allow() for _ in range(500))
    assert window.allow() is False


def test_minute_window_rollover_restores_capacity(fake_clock):
    window = minute_window(_limits(), fake_clock)
    for _ in range(30):
        window.allow()
    assert window.allow() is False
    fake_clock.advance(61)
    assert window.allow() is True


def test_hour_window_rollover_restores_capacity(fake_clock):
    window = hour_window(_limits(), fake_clock)
    for _ in range(500):
        window.allow()
    assert window.allow() is False
    fake_clock.advance(3601)
    assert window.allow() is True
