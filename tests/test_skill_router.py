"""TDD tests for the skill router (tasks 14.018, 14.020)."""

from archlens.vault.skill_router import Skill, load_skills, route


def _skills():
    return [
        Skill("graph-reading",
              ("which module imports", "rank hot nodes", "hot.md triage", "find the hub"), True),
        Skill("refactor",
              ("split god module", "break bottleneck", "merge duplicates", "fix spof"), False),
    ]


def test_load_skills_from_directory_and_route(tmp_path):
    (tmp_path / "SKILL_x.md").write_text(
        "---\nname: x\ndescription: d\nallowed-tools: [Read]\ntriggers: [foo bar]\n---\n",
        encoding="utf-8")
    skills = load_skills(tmp_path)
    assert [s.name for s in skills] == ["x"]
    assert route("please do foo bar", skills) == "x"


def test_exact_trigger_routes_to_skill():
    assert route("Which module imports auth?", _skills()) == "graph-reading"


def test_ambiguous_no_trigger_returns_none():
    assert route("tell me about the weather", _skills()) is None


def test_multiple_matches_is_ambiguous():
    skills = [Skill("a", ("graph",), True), Skill("b", ("graph",), True)]
    assert route("graph stuff", skills) is None


def test_disable_model_invocation_never_auto_returned():
    assert route("please split god module now", _skills()) is None


def test_routing_precision_on_twenty_prompts():
    """Expected (informational): >= 18/20 routed correctly, 0 human-only auto-invocations."""
    skills = _skills()
    graph_prompts = ["which module imports requests", "rank hot nodes for me",
                     "do a hot.md triage", "find the hub of the graph",
                     "which module imports json", "rank hot nodes by degree",
                     "hot.md triage please", "find the hub node"]
    distractors = ["what's the weather", "tell me a joke", "translate this",
                   "summarize the news", "what time is it"]
    human_only = ["split god module", "break bottleneck", "merge duplicates",
                  "fix spof", "split god module now", "break bottleneck here", "fix spof asap"]
    correct = sum(route(p, skills) == "graph-reading" for p in graph_prompts)
    correct += sum(route(p, skills) is None for p in distractors)
    correct += sum(route(p, skills) is None for p in human_only)  # never auto-return refactor
    assert correct >= 18
    assert all(route(p, skills) != "refactor" for p in human_only)
