"""Retry policy with config-driven backoff over the injectable Clock (tasks 9.023, 9.024).

Transient UpstreamAPIErrors are retried up to max_retries, sleeping retry_after_seconds between
attempts (virtual time under FakeClock). On exhaustion the request is handed to on_exhausted
(requeue) so the caller never sees an exception — honouring the never-reject contract.
"""

from .errors import RetryExhaustedSignal, UpstreamAPIError


class RetryPolicy:
    """Retry a transient operation max_retries times with retry_after backoff."""

    def __init__(self, max_retries: int, retry_after_seconds: float, clock):
        self._max = max_retries
        self._wait = retry_after_seconds
        self._clock = clock

    @classmethod
    def from_config(cls, limits, clock) -> "RetryPolicy":
        """Build from a ServiceLimits block (max_retries, retry_after_seconds)."""
        return cls(limits.max_retries, limits.retry_after_seconds, clock)

    def run(self, operation, on_exhausted=None):
        """Run operation with retries; on exhaustion call on_exhausted or raise RetryExhaustedSignal."""
        last: UpstreamAPIError | None = None
        for attempt in range(1, self._max + 1):
            try:
                return operation()
            except UpstreamAPIError as exc:
                last = exc
                if attempt < self._max:
                    self._clock.sleep(self._wait)
        if on_exhausted is not None:
            return on_exhausted(last)
        raise RetryExhaustedSignal(f"retries exhausted after {self._max} attempts") from last
