"""TDD tests for the SDK exception taxonomy (tasks 8.007-8.008)."""

import pytest

from archlens.shared.exceptions import (
    AnalysisError,
    ArchLensError,
    ConfigError,
    GatekeeperError,
    GraphifyError,
    QAGateError,
    RefactorError,
    RepoError,
    TokenBudgetError,
)

SUBCLASSES = [
    ConfigError, RepoError, GraphifyError, AnalysisError,
    RefactorError, QAGateError, GatekeeperError, TokenBudgetError,
]


@pytest.mark.parametrize("cls", SUBCLASSES)
def test_subclass_derives_from_base(cls):
    assert issubclass(cls, ArchLensError)


@pytest.mark.parametrize("cls", SUBCLASSES)
def test_each_has_a_machine_readable_code(cls):
    assert cls.code.startswith("ARCHLENS-")


def test_carries_source_context():
    err = ConfigError("bad key", source_context="setup.json:graphify")
    assert err.source_context == "setup.json:graphify"
    assert isinstance(err, ArchLensError)


def test_codes_are_unique():
    codes = [cls.code for cls in SUBCLASSES]
    assert len(set(codes)) == len(codes)
