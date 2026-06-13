"""TDD tests for vault validation: orphans, broken links, aggregate report (5.032-5.036)."""

from archlens.vault.builder import build_vault
from archlens.vault.validate import find_broken_links, find_orphans, validate_vault


def test_report_clean_on_built_vault(vault_graph, vault_cfg):
    report = validate_vault(build_vault(vault_graph, vault_cfg))
    assert report.ok
    assert report.orphans == []
    assert report.broken_links == []


def test_orphans(vault_graph, vault_cfg):
    layout = build_vault(vault_graph, vault_cfg)
    (layout.wiki_dir / "orphan.md").write_text("# Orphan note\n", encoding="utf-8")
    assert "orphan" in find_orphans(layout)


def test_broken_links(vault_graph, vault_cfg):
    layout = build_vault(vault_graph, vault_cfg)
    (layout.wiki_dir / "payments.md").write_text(
        "# Community: payments\n\n[[ghost]]\n", encoding="utf-8"
    )
    assert any(target == "ghost" for _src, target in find_broken_links(layout))


def test_report_flags_seeded_orphan(vault_graph, vault_cfg):
    layout = build_vault(vault_graph, vault_cfg)
    (layout.wiki_dir / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
    report = validate_vault(layout)
    assert not report.ok
    assert "orphan" in report.orphans
