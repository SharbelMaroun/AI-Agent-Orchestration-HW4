"""FIFO overflow queue with blocking backpressure — never rejects (tasks 9.026, 9.028).

A deque guarded by a Condition: enqueue blocks while at max depth (backpressure) rather than
dropping, so dropped_count stays 0 under saturation. Depth is exposed as a gauge.
"""

import logging
import threading
from collections import deque

from ..shared.constants import LOGGER_NAME

logger = logging.getLogger(f"{LOGGER_NAME}.overflow_queue")


class OverflowQueue:
    """Bounded FIFO queue; enqueue blocks at capacity instead of rejecting."""

    def __init__(self, max_depth: int, warn_ratio: float = 0.0):
        self._capacity = max_depth
        self._warn_at = int(max_depth * warn_ratio) if warn_ratio else 0
        self._items: deque = deque()
        self._cond = threading.Condition()
        self.dropped_count = 0
        self.backpressure_alerts = 0  # monitorable count of warn-ratio crossings
        self._warned = False

    def _maybe_warn(self, depth: int) -> None:
        """Raise a one-shot backpressure alert (gauge + log) when depth crosses the warn ratio."""
        if self._warn_at and depth >= self._warn_at and not self._warned:
            self._warned = True
            self.backpressure_alerts += 1
            logger.warning("overflow backpressure: queue depth %d/%d at warn ratio", depth, self._capacity)
        elif depth < self._warn_at:
            self._warned = False  # re-arm so a later re-crossing alerts again

    @property
    def capacity(self) -> int:
        """The configured maximum queue depth."""
        return self._capacity

    def depth(self) -> int:
        """Current number of queued items (backpressure gauge)."""
        with self._cond:
            return len(self._items)

    def enqueue(self, item, timeout: float | None = None) -> None:
        """Append at the tail, blocking while full (never drops). timeout is for tests only."""
        with self._cond:
            while len(self._items) >= self._capacity:
                if not self._cond.wait(timeout):
                    raise TimeoutError("enqueue timed out")
            self._items.append(item)
            self._maybe_warn(len(self._items))
            self._cond.notify_all()

    def dequeue(self, timeout: float | None = None):
        """Pop the head (FIFO), blocking until an item is available."""
        with self._cond:
            while not self._items:
                if not self._cond.wait(timeout):
                    raise TimeoutError("dequeue timed out")
            item = self._items.popleft()
            self._cond.notify_all()
            return item

    def try_dequeue(self):
        """Non-blocking head pop; return None when empty."""
        with self._cond:
            if not self._items:
                return None
            item = self._items.popleft()
            self._cond.notify_all()
            return item
