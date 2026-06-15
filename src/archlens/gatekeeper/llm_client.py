"""LLM client selection — provider-agnostic: real Anthropic or OpenAI API, else the offline mock.

Mode comes from the ``mode`` argument or the ``ARCHLENS_LLM_MODE`` env var:
  live  -- always the real API (errors at call time if no credential resolves)
  mock  -- always the offline mock (no network)
  auto  -- live when a real credential is detected in the environment, else mock (the default)

Provider comes from ``ARCHLENS_LLM_PROVIDER`` (anthropic | openai), or is auto-detected from
whichever key is present (OpenAI only when its key is set and no Anthropic key is). The selected
client is a drop-in: both expose ``create(model, messages, **kwargs)`` returning ``.usage`` + ``.text``.
"""

import os

from .mock_client import MockAnthropicClient

_DUMMY = "dummy"


def _anthropic_credential() -> bool:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    token = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
    return bool((key and _DUMMY not in key.lower()) or token)


def _openai_credential() -> bool:
    key = os.environ.get("OPENAI_API_KEY", "")
    return bool(key and _DUMMY not in key.lower())


def credential_available() -> bool:
    """True when a real (non-placeholder) credential for any supported provider is present."""
    return _anthropic_credential() or _openai_credential()


def resolve_provider() -> str:
    """Active provider: ``ARCHLENS_LLM_PROVIDER`` override, else auto (OpenAI only when it is the
    one key present; Anthropic is the default and wins ties)."""
    chosen = os.environ.get("ARCHLENS_LLM_PROVIDER", "auto").lower()
    if chosen in ("openai", "anthropic"):
        return chosen
    return "openai" if (_openai_credential() and not _anthropic_credential()) else "anthropic"


def resolve_mode(mode: str | None = None) -> str:
    """Resolve the effective LLM mode (live/mock) from the argument, env var, or auto-detection."""
    chosen = (mode or os.environ.get("ARCHLENS_LLM_MODE", "auto")).lower()
    if chosen == "mock":
        return "mock"
    if chosen == "live" or (chosen == "auto" and credential_available()):
        return "live"
    return "mock"


def resolve_model(cfg) -> str:
    """Model for free-form LLM calls: ``ARCHLENS_LLM_MODEL`` override, else the config default.

    OpenAI users set ``ARCHLENS_LLM_MODEL`` (e.g. ``gpt-4o``) in ``.env`` so the model matches the
    provider; otherwise the Anthropic default from ``config/setup.json`` (``metrics.default_model``).
    """
    return os.environ.get("ARCHLENS_LLM_MODEL") or cfg.metrics.default_model


def extract_text(response) -> str:
    """Pull the reply text from any provider's response (mock/OpenAI ``.text``, Anthropic ``.content``)."""
    text = getattr(response, "text", None)
    if text:
        return text
    content = getattr(response, "content", None) or []
    return "".join(getattr(block, "text", "") for block in content)


def select_llm_client(mode: str | None = None):
    """Return a live provider client (Anthropic/OpenAI) or the offline mock, per mode + provider."""
    if resolve_mode(mode) == "live":
        if resolve_provider() == "openai":
            from .openai_client import OpenAIClient

            return OpenAIClient()
        from .live_client import LiveAnthropicClient

        return LiveAnthropicClient()
    return MockAnthropicClient()
