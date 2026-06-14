"""TDD tests for RefactorFixes.mitigate_spof (task 11.024)."""

from pathlib import Path

from archlens.agents.refactor_fixes import RefactorFixes


def _setup(tmp_path: Path):
    spof = tmp_path / "ss.py"
    spof.write_text("def validate(t):\n    return bool(t)\n", encoding="utf-8")
    deps = []
    for i in (1, 2):
        dep = tmp_path / f"c{i}.py"
        dep.write_text(f"from ss import validate\n\nok{i} = validate({i})\n", encoding="utf-8")
        deps.append(dep)
    return spof, deps


def test_mitigate_spof_creates_adapter_seam(tmp_path):
    spof, deps = _setup(tmp_path)
    seam = RefactorFixes().mitigate_spof(spof, deps)
    assert seam.name == "ss_adapter.py"
    assert seam.exists()


def test_mitigate_spof_rewires_dependents_off_exclusive_dep(tmp_path):
    spof, deps = _setup(tmp_path)
    RefactorFixes().mitigate_spof(spof, deps)
    for dep in deps:
        text = dep.read_text(encoding="utf-8")
        assert "from ss_adapter import validate" in text
        assert "from ss import" not in text
