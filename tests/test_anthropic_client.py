"""TDD tests for the Anthropic client wrapper with mocked HTTP (task 9.037)."""

from types import SimpleNamespace

import pytest

from archlens.gatekeeper.anthropic_client import AnthropicClient
from archlens.gatekeeper.errors import (
    RateLimitedError,
    ServerError,
    UpstreamAPIError,
    UpstreamTimeoutError,
)


def _client(transport, key="sk-test"):
    return AnthropicClient(transport, api_key=key)


def test_payload_assembly_carries_model_and_max_tokens():
    captured = {}

    def transport(payload, key):
        captured.update(payload)
        return SimpleNamespace(status=200, text="ok")

    _client(transport).create("claude-opus-4-8", [{"role": "user", "content": "hi"}], max_tokens=50)
    assert captured["model"] == "claude-opus-4-8"
    assert captured["max_tokens"] == 50


def test_429_maps_to_rate_limited():
    with pytest.raises(RateLimitedError):
        _client(lambda p, k: SimpleNamespace(status=429)).create("m", [])


def test_500_maps_to_server_error():
    with pytest.raises(ServerError):
        _client(lambda p, k: SimpleNamespace(status=500)).create("m", [])


def test_timeout_maps_to_upstream_timeout():
    def transport(payload, key):
        raise TimeoutError("slow")

    with pytest.raises(UpstreamTimeoutError):
        _client(transport).create("m", [])


def test_error_classes_are_upstream_api_errors():
    assert issubclass(RateLimitedError, UpstreamAPIError)
    assert issubclass(ServerError, UpstreamAPIError)
    assert issubclass(UpstreamTimeoutError, UpstreamAPIError)


def test_api_key_read_from_environment(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-env-value")
    captured = {}

    def transport(payload, key):
        captured["key"] = key
        return SimpleNamespace(status=200, text="ok")

    AnthropicClient(transport).create("m", [])
    assert captured["key"] == "sk-env-value"
