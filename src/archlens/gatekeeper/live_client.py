"""Live Anthropic client — routes create() to the real API (used only when a credential resolves).

Credentials are resolved by the official SDK from the environment (ANTHROPIC_API_KEY,
ANTHROPIC_AUTH_TOKEN, or an `ant auth login` profile); no key is ever read or stored here directly.
Upstream failures are mapped to the gatekeeper error types so the retry/queue policy applies.
"""

from .errors import RateLimitedError, ServerError, UpstreamAPIError, UpstreamTimeoutError

_DEFAULT_MAX_TOKENS = 1024


class LiveAnthropicClient:
    """Calls the real Anthropic Messages API; returns the SDK Message (carries `.usage`)."""

    def __init__(self, max_tokens: int = _DEFAULT_MAX_TOKENS):
        import anthropic

        self._client = anthropic.Anthropic()
        self._max_tokens = max_tokens

    def create(self, model, messages, **kwargs):
        """Send one request to the live API, mapping upstream errors to retryable gatekeeper types."""
        import anthropic

        try:
            return self._client.messages.create(
                model=model, messages=messages,
                max_tokens=kwargs.get("max_tokens", self._max_tokens))
        except anthropic.APITimeoutError as exc:
            raise UpstreamTimeoutError(str(exc)) from exc
        except anthropic.RateLimitError as exc:
            raise RateLimitedError(str(exc)) from exc
        except anthropic.APIStatusError as exc:
            if exc.status_code >= 500:
                raise ServerError(str(exc)) from exc
            raise UpstreamAPIError(str(exc)) from exc
