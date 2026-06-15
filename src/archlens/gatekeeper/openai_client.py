"""Live OpenAI client — the provider-agnostic alternative to LiveAnthropicClient.

Selected by select_llm_client when an OpenAI credential/provider is active. Credentials are
resolved by the official SDK from the environment only (OPENAI_API_KEY); no key is read or stored
here. The response is normalized to the same shape every caller already relies on — `.usage`
(input_tokens/output_tokens) plus `.text` — so OpenAI is a drop-in for the Anthropic client.
Upstream failures map to the gatekeeper error types so the retry/queue policy applies.
"""

from types import SimpleNamespace

from .errors import RateLimitedError, ServerError, UpstreamAPIError, UpstreamTimeoutError

_DEFAULT_MAX_TOKENS = 1024


def _normalize(response, model: str):
    """Adapt an OpenAI chat completion to the canonical (.usage.*, .text) response shape."""
    usage = getattr(response, "usage", None)
    in_tokens = getattr(usage, "prompt_tokens", 0)
    out_tokens = getattr(usage, "completion_tokens", 0)
    choices = getattr(response, "choices", None) or []
    text = choices[0].message.content if choices else ""
    return SimpleNamespace(
        status=200, text=text, model=model,
        usage=SimpleNamespace(input_tokens=in_tokens, output_tokens=out_tokens))


class OpenAIClient:
    """Calls the real OpenAI Chat Completions API; returns a canonical response object."""

    def __init__(self, max_tokens: int = _DEFAULT_MAX_TOKENS):
        import openai

        self._client = openai.OpenAI()
        self._max_tokens = max_tokens

    def create(self, model, messages, **kwargs):
        """Send one request to the live API, mapping upstream errors to retryable gatekeeper types."""
        import openai

        try:
            response = self._client.chat.completions.create(
                model=model, messages=messages,
                max_tokens=kwargs.get("max_tokens", self._max_tokens))
            return _normalize(response, model)
        except openai.APITimeoutError as exc:
            raise UpstreamTimeoutError(str(exc)) from exc
        except openai.RateLimitError as exc:
            raise RateLimitedError(str(exc)) from exc
        except openai.APIStatusError as exc:
            if getattr(exc, "status_code", 500) >= 500:
                raise ServerError(str(exc)) from exc
            raise UpstreamAPIError(str(exc)) from exc
