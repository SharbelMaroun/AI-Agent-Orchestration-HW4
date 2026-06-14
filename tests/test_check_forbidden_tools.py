"""Tests for the forbidden-tooling scanner (task 16.003)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_forbidden_tools.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_forbidden_tools", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_repo_is_clean_of_forbidden_tooling():
    assert _load().scan() == []


def test_seeded_command_flagged():
    mod = _load()
    assert mod.is_violation("pip install requests")
    assert mod.is_violation("python -m venv .venv")
    assert mod.is_violation("see requirements.txt")


def test_prohibition_statements_allowlisted():
    mod = _load()
    assert not mod.is_violation("pip and virtualenv are forbidden; use uv")
    assert not mod.is_violation("no requirements.txt anywhere in the repo")
