"""Graphify subprocess egress — the only module allowed to spawn the Graphify binary."""

import subprocess

from archlens.graphops.errors import GraphifyNotFoundError, GraphifyStageError


def run_command(argv: list[str], label: str, timeout_s: int) -> str:
    """Run a Graphify command; return stdout, raise typed errors on failure."""
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s)
    except FileNotFoundError as exc:
        raise GraphifyNotFoundError(f"graphify binary not found: {argv[:2]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise GraphifyStageError(label, f"timed out after {timeout_s}s") from exc
    if proc.returncode != 0:
        raise GraphifyStageError(label, proc.stderr or proc.stdout)
    return proc.stdout
