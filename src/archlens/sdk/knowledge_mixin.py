"""SDK knowledge-asset methods (Phase 14) — a mixin to honour the 150-line file cap."""

from ..vault.skill_guardrails import classify
from ..vault.skill_router import load_skills, route
from ..vault.skill_schema import validate_skill as _validate_skill


class KnowledgeMixin:
    """Phase 14 skill-validation and routing entry points on the SDK facade."""

    def validate_skill(self, path) -> list[str]:
        """Validate a SKILL.md file; return error strings (empty list = valid)."""
        return _validate_skill(path)

    def skill_guardrail(self, path) -> str:
        """Return the guardrail level of a SKILL.md file (auto/reversible/irreversible/human_only)."""
        return classify(path)

    def route_skill(self, prompt: str, skills_dir=None) -> str | None:
        """Route a prompt to a skill name from the configured skills directory."""
        root = skills_dir if skills_dir is not None else self._config().knowledge_assets.skills_dir
        return route(prompt, load_skills(root))

    def build_wiki(self, sources, topics: dict, vault_root):
        """Run the raw->wiki->index pipeline, journaling one log entry per stage; return the root."""
        from pathlib import Path

        from ..vault.index_builder import build_index
        from ..vault.raw_ingest import ingest_with_provenance
        from ..vault.wiki_builder import build_wiki_pages
        from ..vault.wiki_log import append_log

        root = Path(vault_root)
        root.mkdir(parents=True, exist_ok=True)
        log_path = root / "log.md"
        ingested = ingest_with_provenance(root / "raw", sources)
        append_log(log_path, "raw", "ingest", f"{len(ingested)} sources")
        pages = build_wiki_pages(root / "raw", root / "wiki")
        append_log(log_path, "wiki", "build", f"{len(pages)} pages")
        build_index(root / "index.md", topics)
        append_log(log_path, "index", "build", f"{len(topics)} topics")
        return root
