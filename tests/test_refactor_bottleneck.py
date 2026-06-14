"""TDD tests for RefactorFixes.break_bottleneck (task 11.020)."""

from pathlib import Path

from archlens.agents.refactor_fixes import RefactorFixes


def _setup(tmp_path: Path):
    bottleneck = tmp_path / "bottleneck.py"
    bottleneck.write_text("def serve(x):\n    return x\n", encoding="utf-8")
    deps = []
    for i in (1, 2):
        dep = tmp_path / f"d{i}.py"
        dep.write_text(f"from bottleneck import serve\n\nv{i} = serve({i})\n", encoding="utf-8")
        deps.append(dep)
    return bottleneck, deps


def test_break_bottleneck_creates_interface_seam(tmp_path):
    bottleneck, deps = _setup(tmp_path)
    seam = RefactorFixes().break_bottleneck(bottleneck, deps)
    assert seam.name == "bottleneck_interface.py"
    assert seam.exists()


def test_break_bottleneck_rewires_dependents(tmp_path):
    bottleneck, deps = _setup(tmp_path)
    RefactorFixes().break_bottleneck(bottleneck, deps)
    for dep in deps:
        text = dep.read_text(encoding="utf-8")
        assert "from bottleneck_interface import serve" in text
        assert "from bottleneck import" not in text


def test_break_bottleneck_keeps_original_module(tmp_path):
    bottleneck, deps = _setup(tmp_path)
    RefactorFixes().break_bottleneck(bottleneck, deps)
    assert bottleneck.exists()
    assert "def serve" in bottleneck.read_text(encoding="utf-8")
