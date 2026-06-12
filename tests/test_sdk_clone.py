"""TDD tests for the SDK clone_target_repo entry point with the gatekeeper mocked (task 3.025)."""

import json
from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.config import SetupConfig


class FakeGatekeeper:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def git_clone(self, repo, dest: Path) -> Path:
        self.calls.append((repo.url, str(dest)))
        dest.mkdir(parents=True, exist_ok=True)
        return dest


def _cfg(setup_json: Path, tmp_path: Path) -> SetupConfig:
    data = json.loads(setup_json.read_text(encoding="utf-8"))
    data["target_repo"]["workdir_root"] = str(tmp_path / "runs")
    data["fallback_repo"]["workdir_root"] = str(tmp_path / "runs")
    return SetupConfig.model_validate(data)


def test_clone_delegates_to_gatekeeper_exactly_once(setup_json, tmp_path):
    gk = FakeGatekeeper()
    sdk = ArchLensSDK(setup=_cfg(setup_json, tmp_path), gatekeeper=gk)
    path = sdk.clone_target_repo("run1")
    assert len(gk.calls) == 1
    assert path.name == "target"
    assert path.is_relative_to(tmp_path / "runs")


def test_clone_fallback_uses_fallback_repo_block(setup_json, tmp_path):
    cfg = _cfg(setup_json, tmp_path)
    gk = FakeGatekeeper()
    sdk = ArchLensSDK(setup=cfg, gatekeeper=gk)
    sdk.clone_target_repo("run2", use_fallback=True)
    assert gk.calls[0][0] == cfg.fallback_repo.url
