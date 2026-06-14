"""Offline mock LLM client and client selector (task 9.041).

Selected by a config/runtime flag so the full suite runs offline: canned responses with
deterministic token counts and zero network sockets.
"""

from types import SimpleNamespace


def _estimate_input_tokens(messages) -> int:
    """Rough token estimate (~4 chars/token) over the message contents."""
    chars = sum(len(str(message.get("content", ""))) for message in messages)
    return max(1, chars // 4)


class MockAnthropicClient:
    """Returns canned responses with deterministic token counts; opens no sockets.

    With ``estimate=True`` the input-token count is derived from the actual message size, so
    offline measurement runs record realistic context costs (task 12.018/12.021).
    """

    def __init__(self, text: str = "canned response", input_tokens: int = 10,
                 output_tokens: int = 5, estimate: bool = False):
        self._text = text
        self._input_tokens = input_tokens
        self._output_tokens = output_tokens
        self._estimate = estimate

    def create(self, model, messages, **kwargs):
        """Return a deterministic canned response shaped like the real client's."""
        in_tokens = _estimate_input_tokens(messages) if self._estimate else self._input_tokens
        usage = SimpleNamespace(input_tokens=in_tokens, output_tokens=self._output_tokens)
        return SimpleNamespace(status=200, text=self._text, model=model, usage=usage)


def select_client(mock_mode: bool, transport=None, **canned):
    """Return the mock client when mock_mode is set, else the real AnthropicClient."""
    if mock_mode:
        return MockAnthropicClient(**canned)
    from .anthropic_client import AnthropicClient

    return AnthropicClient(transport)
