"""Tests for the interactive repo picker — number/URL resolution and the prompt listing."""

from types import SimpleNamespace

from archlens.repo_picker import pick_repo, resolve_choice


def _repos():
    return [
        SimpleNamespace(name="httpie", url="https://github.com/httpie/cli", note="primary"),
        SimpleNamespace(name="requests", url="https://github.com/psf/requests", note=""),
    ]


def test_resolve_choice_by_number():
    assert resolve_choice("2", _repos()) == "https://github.com/psf/requests"


def test_resolve_choice_accepts_a_pasted_url():
    assert resolve_choice("https://github.com/me/myrepo", _repos()) == "https://github.com/me/myrepo"


def test_resolve_choice_out_of_range_is_none():
    assert resolve_choice("9", _repos()) is None


def test_resolve_choice_garbage_is_none():
    assert resolve_choice("not-a-choice", _repos()) is None


def test_pick_repo_lists_options_and_reads_a_number():
    out = []
    url = pick_repo(_repos(), input_fn=lambda _prompt: "1", output_fn=out.append)
    assert url == "https://github.com/httpie/cli"
    assert any("httpie" in line for line in out)  # the menu was shown
