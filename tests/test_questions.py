"""TDD tests for the standard questions loader (task 12.015)."""

import json

import pytest

from archlens.metrics.questions import load_questions


def test_loads_exactly_ten_unique_questions():
    questions = load_questions()
    assert len(questions) == 10
    assert len({q.id for q in questions}) == 10


def test_every_question_has_non_empty_text_and_evidence():
    for question in load_questions():
        assert question.text.strip()
        assert question.expected_evidence.strip()


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_questions(tmp_path / "nope.json")


def test_duplicate_ids_raise(tmp_path):
    bad = tmp_path / "questions.json"
    dup = {"id": "Q01", "text": "t", "expected_evidence": "hub"}
    bad.write_text(json.dumps({"version": "1.00", "questions": [dup, dup]}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_questions(bad)
