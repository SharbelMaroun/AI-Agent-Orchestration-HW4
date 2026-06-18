"""Standard architecture questions loader (task 12.016).

The same ten questions (Q01-Q10) drive both the baseline and assisted protocols so their
token costs are directly comparable. Loaded from config/questions.json; nothing is hardcoded.
"""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from ..shared.config import check_config_version
from ..shared.constants import QUESTIONS_FILE


class Question(BaseModel):
    """One standard architecture question shared by both measurement protocols."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    expected_evidence: str = Field(min_length=1)


def load_questions(path: str | Path = QUESTIONS_FILE) -> list[Question]:
    """Load and validate the standard questions; raise on missing file or duplicate ids."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"questions file not found: {source}")
    raw = json.loads(source.read_text(encoding="utf-8"))
    check_config_version(raw.get("version", ""), source)  # runtime config-version match (R7)
    questions = [Question.model_validate(item) for item in raw["questions"]]
    ids = [q.id for q in questions]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate question ids in questions.json")
    return questions
