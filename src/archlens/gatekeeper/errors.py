"""Gatekeeper error taxonomy (task 9.013).

RetryExhaustedSignal and QueueSaturationSignal are INTERNAL signals — the never-reject design
keeps them from ever escaping to callers; they drive requeue/backpressure instead.
ConfigVersionError is re-exported from shared.config so callers see one boot-version error type.
"""

from ..shared.config import ConfigVersionError

__all__ = [
    "GatekeeperError",
    "ConfigVersionError",
    "UpstreamAPIError",
    "RetryExhaustedSignal",
    "QueueSaturationSignal",
]


class GatekeeperError(Exception):
    """Base class for every gatekeeper failure."""


class UpstreamAPIError(GatekeeperError):
    """The upstream API returned an error (429 / 5xx / timeout) mapped from the client."""


class RetryExhaustedSignal(GatekeeperError):  # noqa: N818 — internal signal, name fixed by spec
    """Internal: all retries failed; the request is requeued rather than raised to the caller."""


class QueueSaturationSignal(GatekeeperError):  # noqa: N818 — internal signal, name fixed by spec
    """Internal: the overflow queue is at capacity; enqueue blocks rather than rejecting."""
