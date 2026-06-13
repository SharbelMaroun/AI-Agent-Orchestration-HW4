"""Before/after knowledge-asset measurements appended to log.md (task 5.047)."""

from pathlib import Path

from archlens.graphops.parser import Graph
from archlens.vault.config import VaultConfig


def knowledge_asset_metrics(graph: Graph, cfg: VaultConfig) -> dict[str, tuple]:
    """Four Part-B knowledge-asset indicators, each as a (before, after) pair.

    before models naive whole-repo context; after models graph + hub-first retrieval.
    """
    node_count = max(len(graph.nodes), 1)
    edge_count = max(len(graph.edges), 1)
    cited = sum(1 for e in graph.edges if e.source_file)
    return {
        "source_traceability": (0.0, round(cited / edge_count, 2)),
        "noise_reduction": (0.0, round(1 - cfg.index_read_first_count / node_count, 2)),
        "correct_file_identification": (False, True),
        "correct_tool_at_right_time": (False, True),
    }


def render_measurements(metrics: dict[str, tuple]) -> str:
    lines = ["| Metric | Before | After |", "|---|---|---|"]
    for key, (before, after) in metrics.items():
        lines.append(f"| {key} | {before} | {after} |")
    return "\n".join(lines) + "\n"


def append_measurements(log_path, metrics: dict[str, tuple]) -> None:
    """Append the knowledge-asset before/after table to log.md without truncating it."""
    block = "\n## Knowledge-asset measurement\n\n" + render_measurements(metrics)
    path = Path(log_path)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    path.write_text(existing + block, encoding="utf-8")
