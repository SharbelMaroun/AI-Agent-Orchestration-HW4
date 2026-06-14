"""Shared DTO JSON serializer reused by every SDK DTO module (DRY, task 8.013)."""

from dataclasses import asdict, fields

from ..shared.constants import DTO_SCHEMA_VERSION


def to_dict(dto) -> dict:
    """Serialize a frozen DTO to a plain dict, stamping the DTO schema version."""
    data = asdict(dto)
    data["schema_version"] = DTO_SCHEMA_VERSION
    return data


def from_dict(cls, data: dict):
    """Rebuild a DTO from a dict, ignoring schema_version and restoring tuple fields."""
    names = {field.name for field in fields(cls)}
    kwargs = {
        key: (tuple(value) if isinstance(value, list) else value)
        for key, value in data.items()
        if key in names
    }
    return cls(**kwargs)
