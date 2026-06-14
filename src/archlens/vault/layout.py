"""Vault directory layout builder (tasks 5.006-5.007)."""

from dataclasses import dataclass
from pathlib import Path

from ..shared.constants import HOT_MD, INDEX_MD, LOG_MD
from ..vault.config import VaultConfig


@dataclass
class VaultLayout:
    """Resolved vault paths; create() materializes root, raw/, and wiki/."""

    cfg: VaultConfig

    @property
    def root(self) -> Path:
        return Path(self.cfg.vault_root)

    @property
    def raw_dir(self) -> Path:
        return self.root / self.cfg.raw_dir_name

    @property
    def wiki_dir(self) -> Path:
        return self.root / self.cfg.wiki_dir_name

    @property
    def hot_md(self) -> Path:
        return self.root / HOT_MD

    @property
    def index_md(self) -> Path:
        return self.root / INDEX_MD

    @property
    def log_md(self) -> Path:
        return self.root / LOG_MD

    def create(self) -> "VaultLayout":
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.wiki_dir.mkdir(parents=True, exist_ok=True)
        return self
