"""Vault structural validation: orphans, broken wikilinks, aggregate report (5.032-5.036)."""

import re
from dataclasses import dataclass, field

from ..vault.layout import VaultLayout
from ..vault.note_lint import NoteLintError, check_one_idea

_LINK = re.compile(r"\[\[([^\]]+)\]\]")
_NO_INBOUND_OK = {"index", "log"}


@dataclass
class VaultReport:
    """Aggregate structural findings; ok is true only when every list is empty."""

    orphans: list[str] = field(default_factory=list)
    broken_links: list[tuple[str, str]] = field(default_factory=list)
    lint_violations: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not (self.orphans or self.broken_links or self.lint_violations)


def _notes(layout: VaultLayout) -> list:
    raw = layout.raw_dir.resolve()
    return sorted(p for p in layout.root.rglob("*.md") if raw not in p.resolve().parents)


def find_broken_links(layout: VaultLayout) -> list[tuple[str, str]]:
    notes = _notes(layout)
    stems = {p.stem for p in notes}
    broken = []
    for note in notes:
        for target in _LINK.findall(note.read_text(encoding="utf-8")):
            if target not in stems:
                broken.append((note.name, target))
    return broken


def find_orphans(layout: VaultLayout) -> list[str]:
    notes = _notes(layout)
    inbound = {p.stem: 0 for p in notes}
    for note in notes:
        for target in _LINK.findall(note.read_text(encoding="utf-8")):
            if target in inbound and target != note.stem:
                inbound[target] += 1
    return sorted(s for s, n in inbound.items() if n == 0 and s not in _NO_INBOUND_OK)


def validate_vault(layout: VaultLayout) -> VaultReport:
    lint = []
    for note in _notes(layout):
        try:
            check_one_idea(note.read_text(encoding="utf-8"))
        except NoteLintError as exc:
            lint.append(f"{note.name}: {exc}")
    return VaultReport(
        orphans=find_orphans(layout),
        broken_links=find_broken_links(layout),
        lint_violations=lint,
    )
