"""Parse FR-xx / NFR-xx requirement ids and titles from PRD markdown (task 7.019)."""

import re
from dataclasses import dataclass
from pathlib import Path

_REQ = re.compile(r"\*\*(FR-\d+|NFR-\d+)\*\*\s*[—\-–:]\s*(.+)")
_HEADING = re.compile(r"^#+\s+(.*)")


@dataclass(frozen=True)
class Requirement:
    """One requirement id, its title, and the section heading it sits under."""

    id: str
    title: str
    section: str


def _read(source: str | Path) -> str:
    if isinstance(source, Path):
        return source.read_text(encoding="utf-8")
    return source if "\n" in source else Path(source).read_text(encoding="utf-8")


def parse_requirements(source: str | Path) -> list[Requirement]:
    """Extract requirement ids, titles, and their nearest section heading from markdown."""
    section = ""
    out: list[Requirement] = []
    for line in _read(source).splitlines():
        heading = _HEADING.match(line)
        if heading:
            section = heading.group(1).strip()
            continue
        match = _REQ.search(line)
        if match:
            out.append(Requirement(match.group(1), match.group(2).strip().rstrip("."), section))
    return out
