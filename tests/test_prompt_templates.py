"""TDD tests for the 7 agent prompt templates (tasks 10.044-10.045)."""

import re

import pytest

from archlens.agents.prompt_loader import (
    AGENTS,
    declared_variables,
    load_prompt,
    prompt_id,
    render_prompt,
    system_prompt,
    version_of,
)

# Agents that issue an LLM call load their system prompt by id+version (PRD §9 / FR-AO-13).
_LLM_AGENTS = ("analyst", "bughunter", "refactor", "localizer")


@pytest.mark.parametrize("name", AGENTS)
def test_prompt_loads_with_version_header(name):
    assert "Version: 1.00" in load_prompt(name)


@pytest.mark.parametrize("name", _LLM_AGENTS)
def test_llm_prompt_exposes_id_version_and_system(name):
    assert prompt_id(name).startswith("PB-")  # PROMPT_BOOK id, recorded in the token ledger
    assert version_of(name) == "1.00"
    system = system_prompt(name)
    assert system and "Task:" not in system  # the system section only, not the task body


@pytest.mark.parametrize("name", AGENTS)
def test_prompt_renders_with_no_unresolved_placeholders(name):
    values = {variable: f"<{variable}>" for variable in declared_variables(name)}
    assert values, f"{name} declares no variables"
    rendered = render_prompt(name, **values)
    assert re.search(r"\{[A-Za-z_]\w*\}", rendered) is None
