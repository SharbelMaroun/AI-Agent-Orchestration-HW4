"""TDD tests for offline mock mode (task 9.040)."""

from archlens.gatekeeper.anthropic_client import AnthropicClient
from archlens.gatekeeper.mock_client import MockAnthropicClient, select_client


def test_canned_response_is_deterministic():
    client = MockAnthropicClient(input_tokens=12, output_tokens=7)
    first = client.create("m", [])
    second = client.create("m", [])
    assert first.usage.input_tokens == 12
    assert second.usage.output_tokens == 7
    assert first.text == second.text


def test_no_sockets_opened_in_mock_mode(blocked_sockets):
    response = MockAnthropicClient().create("claude-opus-4-8", [{"role": "user", "content": "hi"}])
    assert response.status == 200


def test_select_client_returns_mock_when_flag_set():
    assert isinstance(select_client(mock_mode=True), MockAnthropicClient)


def test_select_client_returns_real_when_flag_unset():
    assert isinstance(select_client(mock_mode=False, transport=lambda p, k: None), AnthropicClient)
