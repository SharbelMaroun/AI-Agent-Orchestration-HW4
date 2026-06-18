"""Rate-limited executor — composes the gatekeeper parts behind execute() (task 9.043).

Wires the per-minute/per-hour windows, concurrency semaphore, retry policy, FIFO overflow queue,
drain loop, call logger, and token ledger into one never-reject entry point. Saturated calls queue
and drain to completion; nothing is ever rejected, and all shared state is lock-guarded.
"""

import logging
import threading

from ..shared.constants import LOGGER_NAME
from .call_log import log_call
from .concurrency import ConcurrencyLimiter
from .ledger import TokenLedger
from .overflow_queue import OverflowQueue
from .rate_config import load_rate_config, service_limits
from .retry import RetryPolicy
from .windows import hour_window, minute_window

logger = logging.getLogger(f"{LOGGER_NAME}.executor")


class _Pending:
    """A queued/dispatched call carrying its request and (eventual) response."""

    __slots__ = ("request", "response")

    def __init__(self, request: dict):
        self.request = request
        self.response = None


class RateLimitedExecutor:
    """Single execute() entry point composing windows, semaphore, retry, queue, log, and ledger."""

    def __init__(self, client, clock, config=None):
        cfg = config or load_rate_config()
        limits = service_limits(cfg)
        self._client = client
        self._clock = clock
        self._minute = minute_window(limits, clock)
        self._hour = hour_window(limits, clock)
        self._semaphore = ConcurrencyLimiter(limits.concurrent_max)
        self._retry = RetryPolicy.from_config(limits, clock)
        self._queue = OverflowQueue(cfg.queue.max_depth, cfg.queue.backpressure_warn_ratio)
        self.ledger = TokenLedger()
        self._lock = threading.Lock()
        self.dispatched = 0

    @property
    def queue_depth(self) -> int:
        return self._queue.depth()

    @property
    def dropped(self) -> int:
        return self._queue.dropped_count

    @property
    def window_counts(self) -> tuple[int, int]:
        return self._minute.count(), self._hour.count()

    def _admit(self) -> bool:
        with self._lock:
            if self._minute.would_allow() and self._hour.would_allow():
                self._minute.record()
                self._hour.record()
                return True
        return False

    def _on_exhausted(self, err: Exception):
        """Retries exhausted: surface a warning (monitoring) and return no response (never raise)."""
        logger.warning("gatekeeper call exhausted retries for model %s: %s",
                       err.__class__.__name__, err)
        return None

    def _dispatch(self, pending: _Pending) -> None:
        with self._semaphore:
            pending.response = self._retry.run(
                lambda: self._client.create(**pending.request), on_exhausted=self._on_exhausted)
        usage = getattr(pending.response, "usage", None)
        in_tokens = getattr(usage, "input_tokens", 0)
        out_tokens = getattr(usage, "output_tokens", 0)
        self.ledger.record(pending.request["model"], in_tokens, out_tokens, 0.0)
        log_call(pending.request["model"], in_tokens, out_tokens, 0, self._queue.depth())
        with self._lock:
            self.dispatched += 1

    def _submit(self, pending: _Pending) -> bool:
        if self._admit():
            self._dispatch(pending)
            return True
        self._queue.enqueue(pending)
        return False

    def submit(self, model, messages, **kwargs) -> bool:
        """Non-blocking: dispatch now if capacity allows, else queue (never reject). Return admitted."""
        return self._submit(_Pending({"model": model, "messages": messages, **kwargs}))

    def drain_queue(self) -> None:
        """Dispatch queued calls in FIFO order as window capacity frees (via the Clock)."""
        while self._queue.depth() > 0:
            if self._admit():
                self._dispatch(self._queue.try_dequeue())
            else:
                self._clock.sleep(self._minute.window_seconds)

    def execute(self, model, messages, **kwargs):
        """Single entry point: dispatch now, or queue and drain to completion; return the response."""
        pending = _Pending({"model": model, "messages": messages, **kwargs})
        if not self._submit(pending):
            self.drain_queue()
        return pending.response
