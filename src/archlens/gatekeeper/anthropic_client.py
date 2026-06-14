"""Anthropic API client wrapper — payload assembly + error mapping (task 9.038).

The key is read only via os.environ.get(ENV_ANTHROPIC_KEY); no key literal or default exists.
The HTTP transport is injected so tests mock it with zero real network. Upstream 429/5xx/timeout
responses are mapped to UpstreamAPIError subclasses for the retry policy.
"""

import os

from ..shared.constants import ENV_ANTHROPIC_KEY
from .errors import RateLimitedError, ServerError, UpstreamAPIError, UpstreamTimeoutError

_DEFAULT_MAX_TOKENS = 1024


class AnthropicClient:
    """Assembles request payloads, calls the injected transport, and maps upstream errors."""

    def __init__(self, transport, api_key: str | None = None):
        self._transport = transport
        self._api_key = api_key if api_key is not None else os.environ.get(ENV_ANTHROPIC_KEY)

    def build_payload(self, model, messages, max_tokens: int = _DEFAULT_MAX_TOKENS) -> dict:
        """Assemble the Anthropic messages request payload."""
        return {"model": model, "messages": messages, "max_tokens": max_tokens}

    def create(self, model, messages, **kwargs):
        """Send one request through the transport, mapping upstream failures to typed errors."""
        payload = self.build_payload(model, messages, **kwargs)
        try:
            response = self._transport(payload, self._api_key)
        except TimeoutError as exc:
            raise UpstreamTimeoutError("anthropic request timed out") from exc
        status = getattr(response, "status", 200)
        if status == 429:
            raise RateLimitedError("429 rate limited")
        if status >= 500:
            raise ServerError(f"{status} server error")
        if status >= 400:
            raise UpstreamAPIError(f"{status} client error")
        return response
