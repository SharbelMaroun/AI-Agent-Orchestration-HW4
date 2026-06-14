"""Generic subprocess egress for non-network commands (e.g. uv run pytest in the target repo)."""

import subprocess
from types import SimpleNamespace


def run_capture(argv: list[str], cwd, timeout_s: int) -> SimpleNamespace:
    """Run a command capturing output; return returncode/stdout/stderr (never raises on nonzero)."""
    try:
        proc = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout_s)
        return SimpleNamespace(returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
    except subprocess.TimeoutExpired as exc:
        return SimpleNamespace(returncode=1, stdout=exc.stdout or "", stderr="timeout")
