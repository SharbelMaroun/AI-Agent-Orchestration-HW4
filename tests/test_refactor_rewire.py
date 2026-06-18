"""Package-aware import rewriting + seam re-export (so the seam fix works on real packages)."""

from archlens.agents.refactor_rewire import make_seam, rewrite_import


def test_rewrites_a_relative_import(tmp_path):
    dep = tmp_path / "d.py"
    dep.write_text("from .context import Environment\n", encoding="utf-8")
    assert rewrite_import(dep, "context", "context_interface")
    assert "from .context_interface import Environment" in dep.read_text(encoding="utf-8")


def test_rewrites_a_dotted_package_import(tmp_path):
    dep = tmp_path / "d.py"
    dep.write_text("from package.context import Environment\n", encoding="utf-8")
    rewrite_import(dep, "context", "context_interface")
    assert "from package.context_interface import Environment" in dep.read_text(encoding="utf-8")


def test_rewrites_a_bare_import_and_leaves_unrelated_ones(tmp_path):
    dep = tmp_path / "d.py"
    dep.write_text("from context import x\nfrom other import y\n", encoding="utf-8")
    rewrite_import(dep, "context", "context_interface")
    text = dep.read_text(encoding="utf-8")
    assert "from context_interface import x" in text
    assert "from other import y" in text          # the context substring must not touch `other`


def test_seam_uses_a_relative_reexport_inside_a_package(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    src = pkg / "context.py"
    src.write_text("class Environment:\n    pass\n", encoding="utf-8")
    seam = make_seam(src, [], "interface")
    assert "from .context import *" in seam.read_text(encoding="utf-8")


def test_seam_uses_a_bare_reexport_for_a_flat_module(tmp_path):
    src = tmp_path / "context.py"
    src.write_text("class Environment:\n    pass\n", encoding="utf-8")
    seam = make_seam(src, [], "interface")
    assert "from context import *" in seam.read_text(encoding="utf-8")
