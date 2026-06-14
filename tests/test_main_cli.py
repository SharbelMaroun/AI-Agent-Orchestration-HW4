"""TDD tests for the thin CLI subcommands and the SDK-only import guard (8.033-8.035)."""

from pathlib import Path
from types import SimpleNamespace

import pytest

import archlens
from archlens.__main__ import main


class _FakeSDK:
    def __init__(self):
        self.called = []

    def version(self):
        self.called.append("version")
        return "1.00"

    def analyze(self):
        self.called.append("analyze")
        return "report"

    def run_loop(self):
        self.called.append("loop")
        return "loop_result"

    def measure_tokens(self):
        self.called.append("tokens")
        return "token_report"

    def build_vault(self, graph):
        self.called.append("vault")
        return SimpleNamespace(root="/vault")


@pytest.mark.parametrize("command,marker", [
    ("analyze", "analyze"), ("loop", "loop"), ("tokens", "tokens"), ("vault", "vault"),
])
def test_subcommand_maps_to_sdk_method_and_exits_zero(command, marker):
    sdk = _FakeSDK()
    argv = [command, "g.json"] if command == "vault" else [command]
    assert main(argv, sdk=sdk) == 0
    assert marker in sdk.called


def test_src_main_imports_only_the_sdk_layer():
    main_py = Path(archlens.__file__).resolve().parent.parent / "main.py"
    text = main_py.read_text(encoding="utf-8")
    for forbidden in ("archlens.agents", "archlens.graphops", "archlens.vault", "archlens.metrics"):
        assert forbidden not in text
