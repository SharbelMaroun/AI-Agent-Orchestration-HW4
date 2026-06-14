"""Injectable Clock protocol plus a FakeClock test double (task 9.014).

Every time-dependent gatekeeper component (windows, retry, drain) depends on a Clock so tests
drive time deterministically via FakeClock.advance() with zero real sleeps.
"""

import time
from typing import Protocol


class Clock(Protocol):
    """A time source the gatekeeper depends on (real or fake)."""

    def now(self) -> float:
        """Return the current time in seconds."""
        ...

    def sleep(self, seconds: float) -> None:
        """Block (or advance virtual time) for the given number of seconds."""
        ...


class SystemClock:
    """Real clock backed by time.monotonic / time.sleep."""

    def now(self) -> float:
        return time.monotonic()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


class FakeClock:
    """Deterministic clock: advance()/sleep() move virtual time without any real delay."""

    def __init__(self, start: float = 0.0):
        self._now = start

    def now(self) -> float:
        return self._now

    def sleep(self, seconds: float) -> None:
        self._now += seconds

    def advance(self, seconds: float) -> None:
        """Move virtual time forward without sleeping."""
        self._now += seconds
