from {{ cookiecutter.project_slug }}.domain.services.threshold_service import apply_threshold
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel


def test_apply_threshold_returns_label_with_highest_score() -> None:
    labels = list(PredictionLabel)
    scores = {labels[0].value: 0.3, labels[-1].value: 0.7}
    result = apply_threshold(scores)
    assert result == labels[-1]


def test_apply_threshold_returns_first_label_when_all_zero() -> None:
    labels = list(PredictionLabel)
    scores = {label.value: 0.0 for label in labels}
    result = apply_threshold(scores)
    assert result == labels[0]
