"""Tests for sdk.apply_fix — seam fix when the graph has dependents, else split; safe no-op."""

import json

from archlens.sdk.sdk import ArchLensSDK


def test_apply_fix_splits_a_real_module_and_reports_success(tmp_path):
    module = tmp_path / "god.py"
    module.write_text("def a():\n    return 1\n\n\ndef b():\n    return 2\n", encoding="utf-8")
    ok = ArchLensSDK().apply_fix({"source_file": "god.py", "category": "god_node"}, str(tmp_path))
    assert ok is True
    assert (tmp_path / "god_part1.py").is_file()              # a part was emitted
    assert "import *" in module.read_text(encoding="utf-8")   # original is now a facade


def test_apply_fix_is_a_safe_noop_when_the_file_is_missing(tmp_path):
    assert ArchLensSDK().apply_fix({"source_file": "nope.py"}, str(tmp_path)) is False


def test_apply_fix_inserts_a_seam_and_rewires_dependents_when_the_graph_has_them(tmp_path):
    (tmp_path / "bottleneck.py").write_text("def srv():\n    return 1\n", encoding="utf-8")
    (tmp_path / "user.py").write_text("from bottleneck import srv\n", encoding="utf-8")
    graph = {
        "nodes": [{"id": "srv", "type": "code", "source_file": "bottleneck.py"},
                  {"id": "u", "type": "code", "source_file": "user.py"}],
        "edges": [{"from": "u", "to": "srv", "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.9, "source_file": "user.py"}],
    }
    gj = tmp_path / "graph.json"
    gj.write_text(json.dumps(graph), encoding="utf-8")
    finding = {"id": "validated-srv", "source_file": "bottleneck.py", "category": "god_node"}
    ok = ArchLensSDK().apply_fix(finding, str(tmp_path), str(gj))
    assert ok is True
    assert (tmp_path / "bottleneck_interface.py").is_file()                       # seam created
    assert "bottleneck_interface" in (tmp_path / "user.py").read_text(encoding="utf-8")  # rewired
