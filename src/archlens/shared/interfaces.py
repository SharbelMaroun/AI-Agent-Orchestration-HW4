"""Shared structural interfaces — the gatekeeper egress boundary (task 8.015)."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class GatekeeperProtocol(Protocol):
    """The sole egress boundary: every LLM, subprocess, and HTTP call plus a rate-limit hook."""

    def call_llm(self, prompt: str, **kwargs) -> str:
        """Execute an LLM call through the gatekeeper."""
        ...

    def run_subprocess(self, args, **kwargs):
        """Execute an external subprocess through the gatekeeper."""
        ...

    def http_get(self, url: str, **kwargs):
        """Execute an HTTP GET through the gatekeeper."""
        ...

    def rate_limit_status(self) -> dict:
        """Return the current rate-limit / queue status."""
        ...
