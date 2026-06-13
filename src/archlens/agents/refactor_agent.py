"""RefactorAgent node — plan a fix for the top VALIDATED finding before any write (10.022)."""


def _validated_open(state: dict) -> list[dict]:
    return [f for f in (state.get("findings") or [])
            if f.get("from") == "bughunter" and f.get("level") == "VALIDATED"
            and f.get("status") == "open"]


def make_refactor_node(sdk):
    """Factory: bind the SDK and return the refactor node. Produces a plan only — no write."""

    def refactor_node(state: dict) -> dict:
        candidates = _validated_open(state)
        if not candidates:
            return {}
        target = candidates[0]
        plan = {
            "target": target["source_file"],
            "action": "split_module",
            "rationale": f"address {target['category']} at {target['source_file']}",
        }
        return {"findings": [{**target, "status": "selected", "plan": plan}]}

    return refactor_node
