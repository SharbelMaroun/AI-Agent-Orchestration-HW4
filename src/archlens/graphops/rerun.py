"""Per-iteration Graphify re-run: regenerate graph.json/graph.html/REPORT.md (task 11.030).

The full pipeline (detect→extract→build→cluster→export) is re-run into an iteration-scoped
output dir; the wrapper verifies all three artifacts exist before returning the dir.
"""

from pathlib import Path

from ..shared.constants import GRAPH_HTML, GRAPH_JSON, GRAPHIFY_STAGES, REPORT_MD

_ARTIFACTS = (GRAPH_JSON, GRAPH_HTML, REPORT_MD)


def iteration_output_dir(output_root, iteration: int) -> Path:
    """Create and return the iteration_<NN> artifact directory under output_root."""
    path = Path(output_root) / f"iteration_{iteration:02d}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def rerun_graphify(repo_path, output_root, iteration: int, runner) -> Path:
    """Re-run the full Graphify pipeline for one iteration; return the artifact dir."""
    out = iteration_output_dir(output_root, iteration)
    runner(Path(repo_path), out, list(GRAPHIFY_STAGES))
    missing = [name for name in _ARTIFACTS if not (out / name).is_file()]
    if missing:
        raise FileNotFoundError(f"graphify re-run missing artifacts: {missing}")
    return out
