"""Thread-safe metrics accumulator guarded by a lock (task 8.043)."""

import threading


class MetricsCounter:
    """A lock-guarded counter so concurrent agent runs never lose updates."""

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}
        self._lock = threading.Lock()

    def add(self, key: str, amount: int = 1) -> None:
        with self._lock:
            self._counts[key] = self._counts.get(key, 0) + amount

    def get(self, key: str) -> int:
        with self._lock:
            return self._counts.get(key, 0)

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(self._counts)
