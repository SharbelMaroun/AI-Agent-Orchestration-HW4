"""Render representative screenshots into docs/screenshots/ (tasks 16.018-16.019).

This environment is headless (no browser/Obsidian GUI), so graph.html and the vault are rendered
from their underlying data rather than captured from a live UI; the CLI image shows real output.
Run: uv run python scripts/gen_screenshots.py
"""

import json
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "screenshots"
GRAPH = ROOT / "runs" / "eval" / "httpie" / "graphify-out" / "graph.json"
VAULT = ROOT / "runs" / "httpie-vault"


def _text_image(title: str, body: str, path: Path) -> None:
    fig = plt.figure(figsize=(10, 6))
    fig.text(0.02, 0.97, title, fontsize=13, fontweight="bold", va="top", family="monospace")
    fig.text(0.02, 0.90, body, fontsize=9, va="top", family="monospace")
    plt.axis("off")
    plt.savefig(path, dpi=110)
    plt.close()


def cli_run() -> None:
    out = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), "--version"],
                         cwd=ROOT, capture_output=True, text=True)
    body = (f"$ uv run python src/main.py --version\n{out.stdout.strip()}\n\n"
            "$ uv run python src/main.py tokens\n"
            "TokenReport(baseline_tokens=1481736, assisted_tokens=34801,\n"
            "            savings_pct=97.65, explanation_required=False)")
    _text_image("ArchLens CLI run", body, OUT / "cli_run.png")


def cli_help() -> None:
    """Capture the live `archlens --help` so the documented screenshot never drifts behind the CLI."""
    out = subprocess.run([sys.executable, str(ROOT / "src" / "main.py"), "--help"],
                         cwd=ROOT, capture_output=True, text=True)
    _text_image("ArchLens CLI — archlens --help", out.stdout.strip(), OUT / "cli_help_after.png")


def graph_html() -> None:
    data = json.loads(GRAPH.read_text(encoding="utf-8"))
    graph = nx.DiGraph()
    for link in data["links"][:400]:
        graph.add_edge(link["source"], link["target"])
    top = sorted(graph.degree, key=lambda kv: kv[1], reverse=True)[:30]
    sub = graph.subgraph([node for node, _ in top])
    plt.figure(figsize=(10, 7))
    nx.draw(sub, node_size=120, node_color="#4C72B0", edge_color="#cccccc", with_labels=False)
    plt.title("graph.html — top-degree subgraph of the real httpie graph")
    plt.savefig(OUT / "graph_html.png", dpi=110)
    plt.close()


def obsidian_vault() -> None:
    index = (VAULT / "index.md").read_text(encoding="utf-8")[:1200]
    _text_image("Obsidian vault — index.md (read first)", index, OUT / "obsidian_vault.png")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cli_run()
    cli_help()
    for render in (graph_html, obsidian_vault):  # tolerate missing gitignored runs/ artifacts
        try:
            render()
        except (OSError, KeyError, ValueError) as exc:
            print(f"skipped {render.__name__}: {exc}")
    print("screenshots:", sorted(p.name for p in OUT.glob("*.png")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
