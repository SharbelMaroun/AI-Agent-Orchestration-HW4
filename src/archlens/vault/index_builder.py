"""index.md hub generator — read-first hub grouping 2-3 wiki pages per topic (task 14.026)."""

from pathlib import Path


def build_index(index_path, topics: dict, wiki_dirname: str = "wiki") -> Path:
    """Write index.md: a read-first hub linking 2-3 wiki pages per topic with one-line notes."""
    lines = ["# Index — read first", "",
             "Start here, then open 2-3 wiki pages for the relevant topic.", ""]
    for topic, pages in topics.items():
        lines.append(f"## {topic}")
        for name in list(pages)[:3]:
            lines.append(f"- [{name}]({wiki_dirname}/{name}.md) — {topic} detail")
        lines.append("")
    path = Path(index_path)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
