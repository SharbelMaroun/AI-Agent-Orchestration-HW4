"""TDD tests for the thin CLI entry point (tasks 5.043, 1.034)."""

import pytest

from archlens.__main__ import main
from archlens.sdk.sdk import ArchLensSDK


def test_version_prints_and_exits_zero(capsys):
    assert main(["--version"]) == 0
    assert capsys.readouterr().out.strip() == "1.00"


def test_vault_help_exits_zero():
    with pytest.raises(SystemExit) as exc:
        main(["vault", "--help"])
    assert exc.value.code == 0


def test_vault_subcommand_delegates_to_sdk(monkeypatch, tmp_path):
    captured = {}

    class FakeLayout:
        root = tmp_path / "vault"

    def fake_build(self, graph, raw_sources=None):
        captured["graph"] = graph
        return FakeLayout()

    monkeypatch.setattr(ArchLensSDK, "build_vault", fake_build)
    assert main(["vault", "g.json"]) == 0
    assert captured["graph"] == "g.json"


def test_no_args_prints_help_and_exits_zero(capsys):
    assert main([]) == 0
    assert "archlens" in capsys.readouterr().out
