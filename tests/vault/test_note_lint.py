"""TDD tests for the one-idea-per-note linter (tasks 5.012-5.013)."""

import pytest

from archlens.vault.note_lint import NoteLintError, check_one_idea


def test_single_h1_is_accepted():
    check_one_idea("# Community: payments\n\nbody text\n## Members\n- a\n")


def test_multiple_h1_is_rejected():
    with pytest.raises(NoteLintError):
        check_one_idea("# One\n# Two\n")
