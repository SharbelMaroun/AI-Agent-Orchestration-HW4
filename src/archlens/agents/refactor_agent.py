"""RefactorAgent node — LLM-plan a fix for the top VALIDATED finding and apply it (10.022).

The plan rationale is LLM-authored; the structural change is applied to the clone via
``sdk.apply_fix`` (the SDK is the only writer). On a successful apply the finding is marked
``fixed`` — which is what routes the supervisor back to GraphAgent for the re-graphify + diff.
"""


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
        rationale = sdk.ask_llm(
            f"Propose one concrete, safe refactor to relieve the {target['category']} at "
            f"{target['source_file']}, in one sentence.", agent="RefactorAgent")
        plan = {"target": target["source_file"], "action": "seam_or_split", "rationale": rationale}
        repo_path = (state.get("target_repo") or {}).get("local_path", "")
        graph_json = (state.get("graph_snapshot") or {}).get("graph_json")
        applied = sdk.apply_fix(target, repo_path, graph_json)
        status = "fixed" if applied else "selected"
        return {"findings": [{**target, "status": status, "plan": plan, "applied": applied}]}

    return refactor_node
