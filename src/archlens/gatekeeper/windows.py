"""Sliding-window rate limiters over an injectable Clock (tasks 9.016, 9.018).

Capacities come from config/rate_limits.json (30 req/min, 500 req/hr); no limit literals here.
A request is admitted only while fewer than `capacity` events fall within the trailing window.
"""

from collections import deque

WINDOW_MINUTE_S = 60.0
WINDOW_HOUR_S = 3600.0


class SlidingWindowCounter:
    """Admit up to `capacity` events per trailing `window_seconds`, timed by the Clock."""

    def __init__(self, capacity: int, window_seconds: float, clock):
        self._capacity = capacity
        self._window = window_seconds
        self._clock = clock
        self._events: deque[float] = deque()

    def _evict(self, now: float) -> None:
        while self._events and self._events[0] <= now - self._window:
            self._events.popleft()

    def allow(self) -> bool:
        """Admit one event now if under capacity (recording it); otherwise defer (return False)."""
        now = self._clock.now()
        self._evict(now)
        if len(self._events) >= self._capacity:
            return False
        self._events.append(now)
        return True

    def would_allow(self) -> bool:
        """Check whether an event could be admitted now without recording it."""
        self._evict(self._clock.now())
        return len(self._events) < self._capacity

    def record(self) -> None:
        """Record one admitted event at the current time (pairs with would_allow)."""
        self._events.append(self._clock.now())

    def count(self) -> int:
        """Number of events currently within the window."""
        self._evict(self._clock.now())
        return len(self._events)

    @property
    def window_seconds(self) -> float:
        """The trailing window length in seconds (used by the drain loop to wait out saturation)."""
        return self._window


def minute_window(limits, clock) -> SlidingWindowCounter:
    """Per-minute window sized from limits.requests_per_minute."""
    return SlidingWindowCounter(limits.requests_per_minute, WINDOW_MINUTE_S, clock)


def hour_window(limits, clock) -> SlidingWindowCounter:
    """Per-hour window sized from limits.requests_per_hour."""
    return SlidingWindowCounter(limits.requests_per_hour, WINDOW_HOUR_S, clock)
