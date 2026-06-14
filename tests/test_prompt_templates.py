"""TDD tests for the 7 agent prompt templates (tasks 10.044-10.045)."""

import re

import pytest

from archlens.agents.prompt_loader import AGENTS, declared_variables, load_prompt, render_prompt


@pytest.mark.parametrize("name", AGENTS)
def test_prompt_loads_with_version_header(name):
    assert "Version: 1.00" in load_prompt(name)


@pytest.mark.parametrize("name", AGENTS)
def test_prompt_renders_with_no_unresolved_placeholders(name):
    values = {variable: f"<{variable}>" for variable in declared_variables(name)}
    assert values, f"{name} declares no variables"
    rendered = render_prompt(name, **values)
    assert re.search(r"\{[A-Za-z_]\w*\}", rendered) is None
