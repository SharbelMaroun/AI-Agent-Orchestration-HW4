"""Tests for the SDK free-form LLM facade (ask_llm) and the text/model resolvers."""

from types import SimpleNamespace

from archlens.gatekeeper.llm_client import extract_text, resolve_model
from archlens.sdk.sdk import ArchLensSDK


def test_ask_llm_returns_text_via_the_gatekeeper_in_mock_mode():
    # autouse fixture pins ARCHLENS_LLM_MODE=mock, so this stays offline and deterministic.
    reply = ArchLensSDK().ask_llm("interpret this graph")
    assert reply == "canned response"


def test_extract_text_reads_dot_text_shape():
    assert extract_text(SimpleNamespace(text="hello")) == "hello"


def test_extract_text_reads_anthropic_content_blocks():
    response = SimpleNamespace(content=[SimpleNamespace(text="a"), SimpleNamespace(text="b")])
    assert extract_text(response) == "ab"


def test_extract_text_empty_response_is_empty_string():
    assert extract_text(SimpleNamespace()) == ""


def test_resolve_model_prefers_env_override(monkeypatch):
    monkeypatch.setenv("ARCHLENS_LLM_MODEL", "gpt-4o")
    cfg = SimpleNamespace(metrics=SimpleNamespace(default_model="claude-opus-4-8"))
    assert resolve_model(cfg) == "gpt-4o"


def test_resolve_model_falls_back_to_config_default(monkeypatch):
    monkeypatch.delenv("ARCHLENS_LLM_MODEL", raising=False)
    cfg = SimpleNamespace(metrics=SimpleNamespace(default_model="claude-opus-4-8"))
    assert resolve_model(cfg) == "claude-opus-4-8"
