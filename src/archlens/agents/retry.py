"""Per-node retry wrapper with config-driven max_retries and backoff (task 10.040)."""

import time

from archlens.shared.rate_limits import load_rate_limits


def _config_defaults() -> tuple[int, int]:
    default = load_rate_limits().rate_limits.services.default
    return default.max_retries, default.retry_after_seconds


def with_node_retry(node, max_retries: int | None = None,
                    retry_after: float | None = None, sleep=time.sleep):
    """Wrap a node so retryable errors retry up to max_retries; permanent errors surface at once."""
    if max_retries is None or retry_after is None:
        cfg_max, cfg_after = _config_defaults()
        max_retries = cfg_max if max_retries is None else max_retries
        retry_after = cfg_after if retry_after is None else retry_after

    def wrapped(state: dict) -> dict:
        for attempt in range(max_retries + 1):
            try:
                return node(state)
            except Exception as exc:
                if not getattr(exc, "retryable", False) or attempt == max_retries:
                    raise
                sleep(retry_after)
        return {}

    return wrapped
