"""TDD tests for TestGate exit-code mapping (task 11.026)."""

from types import SimpleNamespace

from archlens.agents.test_gate import FAIL, PASS, TestGate, _gatekeeper_runner


def _runner(code):
    def run(command, cwd):
        return SimpleNamespace(returncode=code, stdout="", stderr="")
    return run


def test_exit_zero_maps_to_pass():
    gate = TestGate(runner=_runner(0))
    assert gate.verdict("repo") == PASS
    assert gate.passed("repo") is True


def test_nonzero_maps_to_fail():
    gate = TestGate(runner=_runner(1))
    assert gate.verdict("repo") == FAIL
    assert gate.passed("repo") is False


def test_runner_receives_uv_run_pytest_and_repo_cwd():
    captured = {}

    def run(command, cwd):
        captured["command"], captured["cwd"] = command, cwd
        return SimpleNamespace(returncode=0)

    TestGate(runner=run).verdict("/tmp/target")
    assert captured["command"][:3] == ["uv", "run", "pytest"]
    assert captured["cwd"] == "/tmp/target"


def test_default_runner_routes_through_gatekeeper():
    assert _gatekeeper_runner(["git", "--version"], ".").returncode == 0
