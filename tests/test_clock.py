"""TDD tests for the injectable Clock protocol and FakeClock (task 9.014)."""

from archlens.gatekeeper.clock import Clock, FakeClock, SystemClock


def test_fake_clock_advance_moves_time_without_real_sleep():
    clock = FakeClock(start=100.0)
    assert clock.now() == 100.0
    clock.advance(61)
    assert clock.now() == 161.0


def test_fake_clock_sleep_advances_virtual_time():
    clock = FakeClock()
    clock.sleep(30)
    assert clock.now() == 30.0


def test_system_clock_now_is_monotonic_non_decreasing():
    clock = SystemClock()
    first = clock.now()
    assert clock.now() >= first


def test_fake_clock_satisfies_clock_protocol():
    clock: Clock = FakeClock()
    assert callable(clock.now) and callable(clock.sleep)
