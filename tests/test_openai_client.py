"""Tests for the provider-agnostic OpenAI client — usage/text normalization + happy-path create."""

from types import SimpleNamespace

from archlens.gatekeeper.openai_client import OpenAIClient, _normalize


def _fake_completion(prompt=11, completion=4, content="hello"):
    usage = SimpleNamespace(prompt_tokens=prompt, completion_tokens=completion)
    choices = [SimpleNamespace(message=SimpleNamespace(content=content))]
    return SimpleNamespace(usage=usage, choices=choices)


def test_normalize_maps_openai_usage_and_text_to_canonical_shape():
    out = _normalize(_fake_completion(), "gpt-4o")
    assert out.usage.input_tokens == 11      # OpenAI prompt_tokens -> canonical input_tokens
    assert out.usage.output_tokens == 4      # OpenAI completion_tokens -> canonical output_tokens
    assert out.text == "hello"
    assert out.model == "gpt-4o"


def test_normalize_handles_empty_choices():
    empty = SimpleNamespace(usage=SimpleNamespace(prompt_tokens=1, completion_tokens=0), choices=[])
    assert _normalize(empty, "gpt-4o").text == ""


def test_create_forwards_to_chat_completions_and_normalizes(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-openai-test1234567890")
    client = OpenAIClient()
    client._client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(
            create=lambda **kwargs: _fake_completion(prompt=20, completion=6, content="hi"))))
    result = client.create("gpt-4o", [{"role": "user", "content": "hi"}], max_tokens=16)
    assert (result.usage.input_tokens, result.usage.output_tokens) == (20, 6)
    assert result.text == "hi"
