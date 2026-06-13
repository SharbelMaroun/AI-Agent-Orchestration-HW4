"""TDD tests for the config-driven clone retry policy (tasks 3.043, 3.044)."""

import re
from pathlib import Path

import pytest

from archlens.gatekeeper import git_ops
from archlens.shared.errors import (
    CloneAuthError,
    CloneNetworkError,
    RetryExhaustedError,
)
from archlens.shared.rate_limits import load_rate_limits

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def limits(rate_limits_json):
    return load_rate_limits(rate_limits_json).rate_limits.services.default


def test_retry_parameters_come_from_config_not_source(limits):
    source = Path(git_ops.__file__).read_text(encoding="utf-8")
    assert re.search(r"\b(30|500)\b", source) is None, "hardcoded retry value in git_ops.py"
    assert limits.max_retries == 3 and limits.retry_after_seconds == 30


def test_success_on_third_attempt(limits, tmp_path):
    attempts, sleeps = [], []

    def flaky_runner(repo, dest):
        attempts.append(1)
        if len(attempts) < 3:
            raise CloneNetworkError("transient")

    git_ops.clone_with_retry(None, tmp_path, limits, runner=flaky_runner, sleeper=sleeps.append)
    assert len(attempts) == 3
    assert sleeps == [limits.retry_after_seconds] * 2


def test_exhaustion_after_max_retries(limits, tmp_path):
    attempts = []

    def always_fail(repo, dest):
        attempts.append(1)
        raise CloneNetworkError("transient")

    with pytest.raises(RetryExhaustedError):
        git_ops.clone_with_retry(None, tmp_path, limits, runner=always_fail, sleeper=lambda s: None)
    assert len(attempts) == limits.max_retries


def test_permanent_error_is_not_retried(limits, tmp_path):
    attempts = []

    def auth_fail(repo, dest):
        attempts.append(1)
        raise CloneAuthError("bad credentials")

    with pytest.raises(CloneAuthError):
        git_ops.clone_with_retry(None, tmp_path, limits, runner=auth_fail, sleeper=lambda s: None)
    assert len(attempts) == 1
