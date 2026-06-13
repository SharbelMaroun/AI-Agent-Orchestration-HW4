"""VaultConfig — typed view of the setup.json 'vault' block (task 5.003)."""

from pydantic import BaseModel, ConfigDict


class VaultConfig(BaseModel):
    """Obsidian vault generation settings; every value sourced from setup.json."""

    model_config = ConfigDict(extra="forbid")

    vault_root: str
    raw_dir_name: str
    wiki_dir_name: str
    hot_top_n: int
    index_read_first_count: int
