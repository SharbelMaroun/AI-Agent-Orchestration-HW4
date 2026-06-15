"""TDD tests for the dependency-free QA gate over a cloned repo (run_quality_gates)."""

from archlens.agents.quality_gates import run_quality_gates


def test_clean_tree_is_green(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "b.py").write_text("def f():\n    return 2\n", encoding="utf-8")
    report = run_quality_gates(tmp_path)
    assert report.tests_green is True
    assert report.ruff_violations == 0
    assert report.coverage_pct == 100.0


def test_syntax_error_is_counted_and_not_green(tmp_path):
    (tmp_path / "ok.py").write_text("y = 2\n", encoding="utf-8")
    (tmp_path / "broken.py").write_text("def oops(:\n", encoding="utf-8")  # invalid syntax
    report = run_quality_gates(tmp_path)
    assert report.tests_green is False
    assert report.ruff_violations == 1
    assert report.coverage_pct == 50.0


def test_dotgit_directory_is_ignored(tmp_path):
    (tmp_path / "ok.py").write_text("z = 3\n", encoding="utf-8")
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "hook.py").write_text("nonsense (((", encoding="utf-8")  # must not be scanned
    assert run_quality_gates(tmp_path).tests_green is True


def test_missing_path_is_vacuously_green(tmp_path):
    report = run_quality_gates(tmp_path / "does-not-exist")
    assert report.tests_green is True
    assert report.ruff_violations == 0


def test_none_path_is_vacuously_green():
    assert run_quality_gates(None).tests_green is True
