"""JSONL persistence for the Phase 12 TokenLedger (task 12.007).

Output paths are resolved from the metrics block of config/setup.json; no path is hardcoded.
"""

import json
from dataclasses import asdict
from pathlib import Path

from ..shared.config import SetupConfig, load_setup
from .ledger import TokenLedger
from .ledger_model import TokenLedgerEntry


class LedgerCorruptionError(ValueError):
    """Raised when a JSONL ledger line cannot be parsed into a TokenLedgerEntry."""


def ledger_path(filename: str, setup: SetupConfig | None = None) -> Path:
    """Resolve ``<metrics.output_dir>/<filename>`` from setup.json (no hardcoded paths)."""
    cfg = setup if setup is not None else load_setup()
    return Path(cfg.metrics.output_dir) / filename


def save_ledger(ledger: TokenLedger, path: Path) -> Path:
    """Write each entry as one JSON object per line, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(asdict(entry), sort_keys=True) for entry in ledger.entries]
    path.write_text("".join(f"{line}\n" for line in lines), encoding="utf-8")
    return path


def load_ledger(path: Path) -> TokenLedger:
    """Read a JSONL ledger back into a TokenLedger, raising on any corrupt line."""
    ledger = TokenLedger()
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            ledger.append(TokenLedgerEntry(**json.loads(raw)))
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise LedgerCorruptionError(f"{path}:{lineno}: {exc}") from exc
    return ledger
