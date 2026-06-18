"""RefactorAgent node — LLM-plan a fix for the top VALIDATED finding and apply it (10.022).

Governance is enforced here, on the live mutating path: a finding must clear the EvidenceGate
(allowed level + full citation triple) before it can execute, the apply action is classified by the
three-tier guardrail (read-only / reversible / irreversible), irreversible actions are deferred to
human approval instead of auto-applying, and the SDK writer snapshots files for rollback. The
rationale is LLM-authored FROM THE REAL SOURCE; the structural change goes through ``sdk.apply_fix``
(the SDK is the only writer). On a successful apply the finding is marked ``fixed``.
"""

from ..agents.evidence_gate import EvidenceGate
from ..agents.fix_policy import FixCandidate
from ..agents.guardrails import classify_action, requires_approval
from ..agents.source_reader import read_source_excerpt

_REFACTOR_SYSTEM = (
    "You are a senior software engineer proposing a safe, behaviour-preserving refactor of a Python "
    "module to reduce coupling around a bottleneck. Reference the actual code; prefer extracting an "
    "interface/seam or splitting cohesive groups. Be concrete and brief.")

_CATEGORY_TO_KIND = {
    "SPOF": "spof", "god_node": "bottleneck", "bottleneck": "bottleneck",
    "oversized": "oversized", "duplicate": "duplicate", "misalignment": "misalignment",
}


def _denied_findings(state: dict) -> set:
    return {a.get("finding") for a in (state.get("approvals") or []) if a.get("status") == "denied"}


def _validated_open(state: dict) -> list[dict]:
    denied = _denied_findings(state)
    return [f for f in (state.get("findings") or [])
            if f.get("from") == "bughunter" and f.get("level") == "VALIDATED"
            and f.get("status") == "open" and f.get("id") not in denied]


def _candidate(finding: dict) -> FixCandidate | None:
    """Build a FixCandidate from a finding, or None if it cannot form a valid citation."""
    try:
        return FixCandidate(
            fix_id=finding.get("id", ""),
            kind=_CATEGORY_TO_KIND.get(finding.get("category", ""), "bottleneck"),
            level=finding.get("level", "INFERRED"),
            relation=finding.get("relation", ""),
            confidence=float(finding.get("confidence", 0.0)),
            source_file=finding.get("source_file", ""),
            node_id=finding.get("node_id", finding.get("id", "")),
        )
    except (ValueError, TypeError):
        return None


def make_refactor_node(sdk):
    """Factory: bind the SDK and return the refactor node (evidence-gated, guardrail-governed)."""

    def refactor_node(state: dict) -> dict:
        candidates = _validated_open(state)
        if not candidates:
            return {}
        target = candidates[0]
        candidate = _candidate(target)
        gate = EvidenceGate.from_config(sdk._config())
        if candidate is None or not gate.admits(candidate):
            return {"findings": [{**target, "status": "selected", "blocked_by": "evidence_gate"}]}

        action = f"apply {candidate.kind} fix to {target['source_file']}"
        tier = classify_action(action)
        if requires_approval(action):  # irreversible -> defer to the human-in-the-loop gate
            return {
                "findings": [{**target, "status": "selected"}],
                "approvals": [{"action": action, "finding": target.get("id"),
                               "tier": tier.value, "status": "pending"}],
            }

        repo_path = (state.get("target_repo") or {}).get("local_path", "")
        graph_json = (state.get("graph_snapshot") or {}).get("graph_json")
        code = read_source_excerpt(repo_path, target["source_file"])
        body = f"\n\n```python\n{code}\n```" if code else ""
        rationale = sdk.ask_llm(
            f"Propose a concrete, behaviour-preserving refactor to relieve the {target['category']} "
            f"at {target['source_file']}.{body}\n\nGive 2-3 specific steps (what to extract or split, "
            "and why it lowers coupling).", system=_REFACTOR_SYSTEM, agent="RefactorAgent",
            max_tokens=500)
        plan = {"target": target["source_file"], "action": "seam_or_split", "rationale": rationale}
        applied = sdk.apply_fix(target, repo_path, graph_json)
        status = "fixed" if applied else "selected"
        return {
            "findings": [{**target, "status": status, "plan": plan, "applied": applied}],
            "approvals": [{"action": action, "finding": target.get("id"),
                           "tier": tier.value, "status": "auto-approved"}],
        }

    return refactor_node
