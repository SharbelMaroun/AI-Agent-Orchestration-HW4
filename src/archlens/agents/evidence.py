"""The BugHunter evidence-ladder output contract (task 10.006)."""

from pydantic import BaseModel, ConfigDict, field_validator

from archlens.shared.constants import CONFIDENCE_MAX, CONFIDENCE_MIN, EVIDENCE_TAGS


class EvidenceFinding(BaseModel):
    """A finding carrying an evidence level and a (relation, confidence, source_file) citation."""

    model_config = ConfigDict(extra="forbid")

    id: str
    category: str
    level: str
    relation: str
    confidence: float
    source_file: str

    @field_validator("level")
    @classmethod
    def _valid_level(cls, value: str) -> str:
        if value not in EVIDENCE_TAGS:
            raise ValueError(f"level must be one of {EVIDENCE_TAGS}: {value}")
        return value

    @field_validator("confidence")
    @classmethod
    def _bounded_confidence(cls, value: float) -> float:
        if not CONFIDENCE_MIN <= value <= CONFIDENCE_MAX:
            raise ValueError(f"confidence {value} outside [{CONFIDENCE_MIN}, {CONFIDENCE_MAX}]")
        return value
