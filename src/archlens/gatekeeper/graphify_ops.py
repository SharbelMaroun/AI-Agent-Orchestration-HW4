"""Graphify subprocess egress — the only module allowed to spawn the Graphify binary."""

import subprocess

from archlens.graphops.errors import GraphifyNotFoundError, GraphifyStageError


def run_stage(argv: list[str], stage: str, timeout_s: int) -> str:
    """Run one Graphify stage command; return stdout, raise typed errors on failure."""
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s)
    except FileNotFoundError as exc:
        raise GraphifyNotFoundError(f"graphify binary not found: {argv[:3]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise GraphifyStageError(stage, f"timed out after {timeout_s}s") from exc
    if proc.returncode != 0:
        raise GraphifyStageError(stage, proc.stderr)
    return proc.stdout
