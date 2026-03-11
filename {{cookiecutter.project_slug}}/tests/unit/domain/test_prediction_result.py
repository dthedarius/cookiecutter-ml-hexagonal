from {{ cookiecutter.project_slug }}.domain.value_objects.confidence_score import ConfidenceScore
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_result import PredictionResult


def test_create_prediction_result() -> None:
    labels = list(PredictionLabel)
    label = labels[0]
    raw_scores = {label.value: 0.5 for label in labels}

    result = PredictionResult(
        label=label,
        confidence=ConfidenceScore(value=0.95),
        raw_scores=raw_scores,
    )
    assert result.label == label
    assert result.confidence.value == 0.95
    assert result.raw_scores == raw_scores
    assert result.metadata == {}


def test_prediction_result_is_frozen() -> None:
    labels = list(PredictionLabel)
    label = labels[0]
    result = PredictionResult(
        label=label,
        confidence=ConfidenceScore(value=0.9),
        raw_scores={label.value: 0.9},
    )
    assert result.label == label
