"""read_source_excerpt feeds agents the real code (bounded), degrading safely when unavailable."""

from archlens.agents.source_reader import read_source_excerpt


def test_reads_the_real_file(tmp_path):
    (tmp_path / "m.py").write_text("class Big:\n    pass\n", encoding="utf-8")
    assert "class Big" in read_source_excerpt(str(tmp_path), "m.py")


def test_truncates_a_large_file(tmp_path):
    (tmp_path / "big.py").write_text("x = 1\n" * 5000, encoding="utf-8")
    out = read_source_excerpt(str(tmp_path), "big.py", max_chars=200)
    assert len(out) <= 260 and "truncated" in out


def test_missing_file_is_empty_string(tmp_path):
    assert read_source_excerpt(str(tmp_path), "nope.py") == ""


def test_blank_inputs_are_empty_string():
    assert read_source_excerpt("", "x.py") == ""
    assert read_source_excerpt("/repo", "") == ""
