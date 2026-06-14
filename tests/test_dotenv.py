"""Tests for the minimal .env loader (set-if-absent, non-empty, skips comments)."""

from archlens.shared.dotenv import load_dotenv


def test_loads_non_empty_keys(tmp_path, monkeypatch):
    monkeypatch.delenv("FOO_KEY", raising=False)
    env = tmp_path / ".env"
    env.write_text("# comment\nFOO_KEY=bar123\nEMPTY_KEY=\n", encoding="utf-8")
    load_dotenv(env)
    import os
    assert os.environ["FOO_KEY"] == "bar123"
    assert "EMPTY_KEY" not in os.environ


def test_does_not_override_existing_env(tmp_path, monkeypatch):
    monkeypatch.setenv("FOO_KEY", "already-set")
    env = tmp_path / ".env"
    env.write_text("FOO_KEY=from-file\n", encoding="utf-8")
    load_dotenv(env)
    import os
    assert os.environ["FOO_KEY"] == "already-set"


def test_missing_file_is_noop(tmp_path):
    load_dotenv(tmp_path / "nope.env")  # must not raise
