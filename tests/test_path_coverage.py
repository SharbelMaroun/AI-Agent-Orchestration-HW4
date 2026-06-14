"""Path-coverage supplement: branch-combination paths through retry and SDK dispatch (task 13.024).

Path IDs (each has a passing parametrized case below):
  PR1 retry: operation succeeds on the first attempt (no backoff).
  PR2 retry: operation fails once, then succeeds within max_retries.
  PR3 retry: operation always fails; on_exhausted handles it without raising.
  PD1 dispatch: `--version` routes to SDK.version().
  PD2 dispatch: `vault <graph>` routes to SDK.build_vault().
  PD3 dispatch: `analyze` routes to SDK.analyze().
  PD4 dispatch: `loop` routes to SDK.run_loop().
  PD5 dispatch: `tokens` routes to SDK.measure_tokens().
  PD6 dispatch: no arguments prints help and returns 0.

Expected: every listed path ID has a passing parametrized case.
"""

import pytest

from archlens.__main__ import main
from archlens.gatekeeper.clock import FakeClock
from archlens.gatekeeper.errors import UpstreamAPIError
from archlens.gatekeeper.retry import RetryPolicy


def _operation_failing(times: int):
    state = {"n": 0}

    def _op():
        if state["n"] < times:
            state["n"] += 1
            raise UpstreamAPIError("transient")
        return "ok"

    return _op


@pytest.mark.parametrize("path_id, fail_times", [("PR1", 0), ("PR2", 1)])
def test_retry_success_paths(path_id, fail_times):
    """Expected: PR1/PR2 return the operation result once it succeeds within max_retries."""
    policy = RetryPolicy(max_retries=3, retry_after_seconds=30, clock=FakeClock())
    assert policy.run(_operation_failing(fail_times)) == "ok"


def test_retry_exhaustion_path_pr3():
    """Expected: PR3 exhausts retries and is handled by on_exhausted, never raising."""
    policy = RetryPolicy(max_retries=3, retry_after_seconds=30, clock=FakeClock())
    assert policy.run(_operation_failing(99), on_exhausted=lambda err: "requeued") == "requeued"


class _StubCLISDK:
    def __init__(self):
        self.called: list[str] = []

    def version(self):
        self.called.append("version")
        return "1.00"

    def build_vault(self, graph):
        self.called.append("vault")
        return type("_Vault", (), {"root": "/v"})()

    def analyze(self):
        self.called.append("analyze")
        return "analysis"

    def run_loop(self):
        self.called.append("loop")
        return "loop"

    def measure_tokens(self):
        self.called.append("tokens")
        return "tokens"


@pytest.mark.parametrize("path_id, argv, expected_call", [
    ("PD1", ["--version"], "version"),
    ("PD2", ["vault", "g.json"], "vault"),
    ("PD3", ["analyze"], "analyze"),
    ("PD4", ["loop"], "loop"),
    ("PD5", ["tokens"], "tokens"),
])
def test_cli_dispatch_paths(path_id, argv, expected_call):
    """Expected: each CLI dispatch path routes to the matching SDK method and returns 0."""
    sdk = _StubCLISDK()
    assert main(argv, sdk=sdk) == 0
    assert expected_call in sdk.called


def test_cli_no_args_help_path_pd6():
    """Expected: PD6 with no arguments returns 0 via the help path."""
    assert main([], sdk=_StubCLISDK()) == 0
