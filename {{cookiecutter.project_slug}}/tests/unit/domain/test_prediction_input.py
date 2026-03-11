import pytest
from pydantic import ValidationError

from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_input import (
    MAX_INPUT_LENGTH,
    PredictionInput,
)


def test_valid_input() -> None:
    result = PredictionInput(text="hello world")
    assert result.text == "hello world"


def test_strips_whitespace() -> None:
    result = PredictionInput(text="  hello  ")
    assert result.text == "hello"


def test_empty_string_raises() -> None:
    with pytest.raises(ValidationError):
        PredictionInput(text="")


def test_whitespace_only_raises() -> None:
    with pytest.raises(ValidationError):
        PredictionInput(text="   ")


def test_exceeds_max_length_raises() -> None:
    with pytest.raises(ValidationError):
        PredictionInput(text="a" * (MAX_INPUT_LENGTH + 1))


def test_at_max_length_ok() -> None:
    result = PredictionInput(text="a" * MAX_INPUT_LENGTH)
    assert len(result.text) == MAX_INPUT_LENGTH
