"""RefactorAgent node — LLM-plan a fix for the top VALIDATED finding and apply it (10.022).

The rationale is LLM-authored FROM THE REAL SOURCE (concrete, code-aware steps); the structural
change is applied to the clone via ``sdk.apply_fix`` (the SDK is the only writer). On a successful
apply the finding is marked ``fixed`` — which routes the supervisor back to GraphAgent for the diff.
"""

from ..agents.source_reader import read_source_excerpt

_REFACTOR_SYSTEM = (
    "You are a senior software engineer proposing a safe, behaviour-preserving refactor of a Python "
    "module to reduce coupling around a bottleneck. Reference the actual code; prefer extracting an "
    "interface/seam or splitting cohesive groups. Be concrete and brief.")


def _validated_open(state: dict) -> list[dict]:
    return [f for f in (state.get("findings") or [])
            if f.get("from") == "bughunter" and f.get("level") == "VALIDATED"
            and f.get("status") == "open"]


def make_refactor_node(sdk):
    """Factory: bind the SDK and return the refactor node (LLM plan + apply via the SDK)."""

    def refactor_node(state: dict) -> dict:
        candidates = _validated_open(state)
        if not candidates:
            return {}
        target = candidates[0]
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
        return {"findings": [{**target, "status": status, "plan": plan, "applied": applied}]}

    return refactor_node
