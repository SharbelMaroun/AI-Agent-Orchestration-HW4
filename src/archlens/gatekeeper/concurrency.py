"""Concurrency limiter — at most concurrent_max in-flight calls (task 9.021).

Backed by a threading.BoundedSemaphore sized from RateLimitConfig.concurrent_max; the 6th
acquirer waits until a slot frees, so observed in-flight never exceeds the cap.
"""

import threading


class ConcurrencyLimiter:
    """A bounded-semaphore gate sized from config; usable as a context manager."""

    def __init__(self, max_concurrent: int):
        self._capacity = max_concurrent
        self._semaphore = threading.BoundedSemaphore(max_concurrent)

    @property
    def capacity(self) -> int:
        """The maximum number of concurrent in-flight calls."""
        return self._capacity

    def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a slot, blocking until one is free (or until timeout)."""
        if timeout is None:
            return self._semaphore.acquire()
        return self._semaphore.acquire(timeout=timeout)

    def release(self) -> None:
        """Release a previously acquired slot."""
        self._semaphore.release()

    def __enter__(self) -> "ConcurrencyLimiter":
        self.acquire()
        return self

    def __exit__(self, *exc) -> bool:
        self.release()
        return False
