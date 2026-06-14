"""Offline mock LLM client and client selector (task 9.041).

Selected by a config/runtime flag so the full suite runs offline: canned responses with
deterministic token counts and zero network sockets.
"""

from types import SimpleNamespace


class MockAnthropicClient:
    """Returns canned responses with deterministic token counts; opens no sockets."""

    def __init__(self, text: str = "canned response", input_tokens: int = 10,
                 output_tokens: int = 5):
        self._text = text
        self._input_tokens = input_tokens
        self._output_tokens = output_tokens

    def create(self, model, messages, **kwargs):
        """Return a deterministic canned response shaped like the real client's."""
        usage = SimpleNamespace(input_tokens=self._input_tokens, output_tokens=self._output_tokens)
        return SimpleNamespace(status=200, text=self._text, model=model, usage=usage)


def select_client(mock_mode: bool, transport=None, **canned):
    """Return the mock client when mock_mode is set, else the real AnthropicClient."""
    if mock_mode:
        return MockAnthropicClient(**canned)
    from .anthropic_client import AnthropicClient

    return AnthropicClient(transport)
