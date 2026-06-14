"""TDD tests for the CLI usability fixes (tasks 16.027/16.028).

Expected: help text is complete (examples + every subcommand), errors are actionable, version works.
"""

import pytest

from archlens.__main__ import _build_parser, main


def test_help_lists_usage_examples():
    """Expected: --help text includes runnable example invocations (H10 fix)."""
    text = _build_parser().format_help()
    assert "Examples:" in text
    assert "uv run python src/main.py" in text


def test_help_names_every_subcommand():
    """Expected: every subcommand appears in the help text."""
    text = _build_parser().format_help()
    for command in ("vault", "deliverables", "analyze", "loop", "tokens"):
        assert command in text


def test_invalid_subcommand_is_actionable():
    """Expected: an invalid subcommand exits non-zero and lists the valid choices."""
    with pytest.raises(SystemExit) as exc:
        main(["definitely-not-a-command"])
    assert exc.value.code != 0


def test_version_flag_prints_and_exits_zero(capsys):
    """Expected: --version prints the version and returns 0."""
    assert main(["--version"]) == 0
    assert "1.00" in capsys.readouterr().out
