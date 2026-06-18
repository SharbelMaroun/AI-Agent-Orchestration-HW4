"""Stop-condition evaluation node and loop-iteration guard (tasks 10.028-10.029).

The five Part C stop conditions (PRD §3.2): SC-1 the bottleneck SHED dependencies (a genuine fix
removes load from the node, Part C p21 / load_shift.dependencies_lost), modularity improved, no new
isolated components, all tests green, ruff zero. ``met`` is the logical AND of all five. This SC-1
polarity matches the LoopController's StopConditionEvaluator (dependency loss is the goal).
"""


def make_stop_eval_node(sdk=None):
    """Factory: return the stop_eval node (sdk unused; verdict is a pure function of state)."""

    def stop_eval_node(state: dict) -> dict:
        diff = (state.get("graph_snapshot") or {}).get("diff") or {}
        qa = state.get("stop_eval") or {}
        verdict = {
            "bottleneck_deps_lost": bool(diff.get("dependency_loss", 0)),
            "modularity_improved": bool(diff.get("modularity_improved", False)),
            "no_new_isolates": not diff.get("new_isolates", False),
            "tests_green": bool(qa.get("tests_green", False)),
            "ruff_zero": bool(qa.get("ruff_zero", False)),
        }
        verdict["met"] = (
            verdict["bottleneck_deps_lost"]  # SC-1: the bottleneck shed dependencies (loss is the goal)
            and verdict["modularity_improved"]
            and verdict["no_new_isolates"]
            and verdict["tests_green"]
            and verdict["ruff_zero"]
        )
        update: dict = {"stop_eval": verdict}
        if not verdict["met"]:
            update["loop_iteration"] = state.get("loop_iteration", 0) + 1
        return update

    return stop_eval_node
