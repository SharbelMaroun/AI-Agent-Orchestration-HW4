"""LLM client selection — real Anthropic API when a credential exists, else the offline mock.

Mode comes from the ``mode`` argument or the ``ARCHLENS_LLM_MODE`` env var:
  live  -- always the real API (errors at call time if no credential resolves)
  mock  -- always the offline mock (no network)
  auto  -- live when a real credential is detected in the environment, else mock (the default)
"""

import os

from .mock_client import MockAnthropicClient

_DUMMY = "dummy"


def credential_available() -> bool:
    """True when a real (non-placeholder) Anthropic credential is present in the environment."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    token = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
    return bool((key and _DUMMY not in key.lower()) or token)


def resolve_mode(mode: str | None = None) -> str:
    """Resolve the effective LLM mode (live/mock) from the argument, env var, or auto-detection."""
    chosen = (mode or os.environ.get("ARCHLENS_LLM_MODE", "auto")).lower()
    if chosen == "mock":
        return "mock"
    if chosen == "live" or (chosen == "auto" and credential_available()):
        return "live"
    return "mock"


def select_llm_client(mode: str | None = None):
    """Return a live Anthropic client (real API) or the offline mock, per mode + credentials."""
    if resolve_mode(mode) == "live":
        from .live_client import LiveAnthropicClient

        return LiveAnthropicClient()
    return MockAnthropicClient()
