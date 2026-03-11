import pytest
from pydantic import ValidationError

from {{ cookiecutter.project_slug }}.domain.value_objects.confidence_score import ConfidenceScore


def test_valid_score() -> None:
    score = ConfidenceScore(value=0.95)
    assert score.value == 0.95


def test_zero_is_valid() -> None:
    score = ConfidenceScore(value=0.0)
    assert score.value == 0.0


def test_one_is_valid() -> None:
    score = ConfidenceScore(value=1.0)
    assert score.value == 1.0


def test_negative_raises() -> None:
    with pytest.raises(ValidationError):
        ConfidenceScore(value=-0.1)


def test_above_one_raises() -> None:
    with pytest.raises(ValidationError):
        ConfidenceScore(value=1.1)
