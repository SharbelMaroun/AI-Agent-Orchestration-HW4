"""Sanity tests for the Phase 13 fixtures (tasks 13.007-13.014).

Expected: each fixture yields the documented layout/behaviour and the autouse guard blocks network.
"""

import socket

import pytest


def test_fixture_repo_layout(fixture_repo):
    """Expected: 3 packages, an import cycle, and one >150-line module exist."""
    assert (fixture_repo / "pkg_a" / "mod.py").is_file()
    assert "import a_fn" in (fixture_repo / "pkg_b" / "mod.py").read_text(encoding="utf-8")
    big = (fixture_repo / "pkg_c" / "big.py").read_text(encoding="utf-8")
    assert len([ln for ln in big.splitlines() if ln.strip()]) > 150


def test_fixture_graph_json_valid(fixture_graph_json):
    """Expected: the sample graph parses with the known node/edge/community counts."""
    data = fixture_graph_json.data
    assert len(data["nodes"]) == 3
    assert len(data["links"]) == 2
    assert {n["community"] for n in data["nodes"]} == {0, 1}


def test_mock_gatekeeper_records_calls(mock_gatekeeper):
    """Expected: the stub records call counts and constructs no real client (task 13.009)."""
    mock_gatekeeper.call_llm("hi")
    mock_gatekeeper.run_subprocess(["pytest"])
    assert len(mock_gatekeeper.calls) == 2


def test_mock_llm_responses_deterministic(mock_llm_responses):
    """Expected: identical prompts return identical canned payloads."""
    assert mock_llm_responses("same") == mock_llm_responses("same")
    assert mock_llm_responses("a") != mock_llm_responses("b")


def test_mock_git_offline_clone(mock_git, tmp_path):
    """Expected: clone writes a tmp_path repo and records the call, no remote."""
    dest = mock_git.clone("https://example.com/x.git", tmp_path / "repo")
    assert (dest / "README.md").is_file()
    assert mock_git.calls[0][0] == "clone"


def test_mock_graphify_artifacts(mock_graphify):
    """Expected: all three pipeline artifacts are written and readable."""
    for name in ("graph.json", "graph.html", "REPORT.md"):
        assert (mock_graphify / name).is_file()


def test_fake_vault_fs_layout(fake_vault_fs):
    """Expected: hot.md, index.md, log.md, and wiki/ all exist."""
    for name in ("hot.md", "index.md", "log.md"):
        assert (fake_vault_fs / name).is_file()
    assert (fake_vault_fs / "wiki").is_dir()


def test_autouse_no_network_blocks_external():
    """Expected: a real outbound connection is blocked by the autouse guard (task 13.014)."""
    with pytest.raises(RuntimeError):
        socket.create_connection(("8.8.8.8", 80), timeout=1)
