"""raw/ -> wiki/ distillation: one wiki page per raw note, each backlinking its raw source (14.024)."""

from pathlib import Path


def _first_meaningful_line(note: Path) -> str:
    for line in note.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if text and not text.startswith(("<!--", "#", "```")):
            return f"Distilled note for `{note.stem}` — {text[:80]}"
    return f"Distilled note for `{note.stem}`."


def build_wiki_pages(raw_dir, wiki_dir) -> list[Path]:
    """Write one distilled wiki page per raw/*.md note, each linking back to its raw source."""
    raw, wiki = Path(raw_dir), Path(wiki_dir)
    wiki.mkdir(parents=True, exist_ok=True)
    pages = []
    for note in sorted(raw.glob("*.md")):
        page = wiki / note.name
        page.write_text(
            f"# {note.stem}\n\n{_first_meaningful_line(note)}\n\n"
            f"_Source:_ [raw/{note.name}](../raw/{note.name})\n",
            encoding="utf-8")
        pages.append(page)
    return pages
