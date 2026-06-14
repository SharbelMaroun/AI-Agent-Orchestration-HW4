"""RefactorAgent fix transformations: split, break bottleneck, merge duplicates, mitigate SPOF.

Covers tasks 11.019/11.021/11.023/11.025. Heavy logic lives in refactor_split / refactor_rewire;
this module is the RefactorAgent-facing API plus the duplicate-merge evidence guard.
"""

from pathlib import Path

from ..shared.constants import DUPLICATE_SIMILARITY_THRESHOLD
from .refactor_rewire import extract_def, make_seam
from .refactor_split import split_module


class RefactorFixes:
    """The four structural fixes the RefactorAgent applies, one per fix-priority class."""

    def split_module(self, path) -> list[Path]:
        """P3: split an oversized module into parts within the line cap."""
        return split_module(path)

    def break_bottleneck(self, bottleneck_path, dependents) -> Path:
        """P2: extract an interface seam and rewire dependents off the bottleneck."""
        return make_seam(bottleneck_path, dependents, "interface")

    def mitigate_spof(self, spof_path, dependents) -> Path:
        """P1: introduce an adapter seam so the SPOF loses its exclusive dependents."""
        return make_seam(spof_path, dependents, "adapter")

    def merge_duplicates(self, pair: dict, shared_path) -> Path:
        """P4: relocate a VALIDATED duplicate (similarity >= 0.91) into a shared module."""
        if pair["level"] != "VALIDATED" or pair["similarity"] < DUPLICATE_SIMILARITY_THRESHOLD:
            raise ValueError("merge requires VALIDATED level and similarity >= threshold")
        shared = Path(shared_path)
        name = pair["func_name"]
        sources = [Path(s) for s in pair["sources"]]
        _, segment = extract_def(sources[0].read_text(encoding="utf-8"), name)
        existing = shared.read_text(encoding="utf-8") if shared.exists() else ""
        shared.write_text(f"{existing}{segment}\n", encoding="utf-8")
        for src in sources:
            remaining, _ = extract_def(src.read_text(encoding="utf-8"), name)
            src.write_text(f"from {shared.stem} import {name}\n{remaining}\n", encoding="utf-8")
        return shared
