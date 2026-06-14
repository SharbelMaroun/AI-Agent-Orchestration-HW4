"""Evidence-ladder language linter and the generation gate (tasks 7.034-7.035)."""

from collections.abc import Iterable

from ..shared.constants import EVIDENCE_TAGS


class EvidenceLintError(ValueError):
    """Raised when a deliverable claim lacks exactly one evidence-ladder tag."""


def _tag_count(claim: str) -> int:
    # Count only bracketed [TAG] markers, so the tag words appearing in prose do not count.
    return sum(claim.count(f"[{tag}]") for tag in EVIDENCE_TAGS)


def lint_claims(claims: Iterable[str]) -> list[str]:
    """Return claims that do not carry exactly one OBSERVED/INFERRED/EXTRACTED/VALIDATED tag."""
    return [claim for claim in claims if _tag_count(claim) != 1]


def enforce_evidence(claims: Iterable[str]) -> None:
    """Raise EvidenceLintError if any claim is untagged or carries more than one tag."""
    violations = lint_claims(claims)
    if violations:
        raise EvidenceLintError(
            f"{len(violations)} claim(s) without exactly one evidence tag: {violations[0]!r}"
        )
