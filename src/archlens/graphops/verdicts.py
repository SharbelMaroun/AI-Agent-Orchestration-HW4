"""Emit one evidence-grounded 3-4 sentence verdict per requirement chain (task 7.032)."""

import json
from dataclasses import dataclass
from pathlib import Path

from ..graphops.traceability import TraceChain


@dataclass(frozen=True)
class Verdict:
    """A per-requirement verdict with its label and evidence-cited sentences."""

    req_id: str
    label: str
    sentences: tuple[str, ...]

    @property
    def text(self) -> str:
        return " ".join(self.sentences)


def generate_verdicts(chains: list[TraceChain], graph_source: dict | str | Path) -> list[Verdict]:
    """One verdict per chain: full traceability when tested, possible gap otherwise."""
    data = graph_source if isinstance(graph_source, dict) else json.loads(
        Path(graph_source).read_text(encoding="utf-8"))
    source_file = {n["id"]: n.get("source_file", n["id"]) for n in data.get("nodes", [])}
    verdicts: list[Verdict] = []
    for chain in chains:
        location = source_file.get(chain.module, chain.module)
        tested = bool(chain.tests)
        label = "full traceability" if tested else "possible gap"
        last = (
            f"Tests {', '.join(chain.tests)} reference it at confidence {chain.test_confidence}."
            if tested else f"No test references {chain.module}, so coverage is unproven."
        )
        sentences = (
            f"Requirement {chain.req_id} maps to module {chain.module}.",
            f"Evidence: implements -> {chain.module_confidence} -> {location}.",
            last,
            f"Verdict: {label}.",
        )
        verdicts.append(Verdict(chain.req_id, label, sentences))
    return verdicts
