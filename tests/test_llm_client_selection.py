"""Tests for LLM client selection — real API when a credential exists, else the offline mock."""

from archlens.gatekeeper.llm_client import credential_available, resolve_mode, select_llm_client
from archlens.gatekeeper.mock_client import MockAnthropicClient


def test_mock_mode_returns_mock():
    assert isinstance(select_llm_client("mock"), MockAnthropicClient)


def test_auto_without_credential_is_mock(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    assert resolve_mode("auto") == "mock"
    assert isinstance(select_llm_client("auto"), MockAnthropicClient)


def test_real_key_makes_auto_go_live(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-real1234567890")
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    assert credential_available()
    assert resolve_mode("auto") == "live"


def test_auth_token_counts_as_credential(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "oauth-token-value")
    assert credential_available()


def test_dummy_key_is_not_a_credential(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-dummy-replace-me")
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    assert not credential_available()


def test_live_mode_builds_a_live_client(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test1234567890")
    from archlens.gatekeeper.live_client import LiveAnthropicClient
    assert isinstance(select_llm_client("live"), LiveAnthropicClient)


def test_live_client_create_returns_message_with_usage(monkeypatch):
    """The live client forwards to the SDK and returns its Message (carries usage)."""
    from types import SimpleNamespace

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test1234567890")
    from archlens.gatekeeper.live_client import LiveAnthropicClient

    client = LiveAnthropicClient()
    message = SimpleNamespace(usage=SimpleNamespace(input_tokens=12, output_tokens=3))
    client._client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kwargs: message))
    result = client.create("claude-opus-4-8", [{"role": "user", "content": "hi"}], max_tokens=16)
    assert result.usage.input_tokens == 12
