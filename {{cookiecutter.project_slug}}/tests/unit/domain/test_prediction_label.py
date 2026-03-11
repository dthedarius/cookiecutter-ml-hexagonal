from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel


def test_prediction_label_has_values() -> None:
    labels = list(PredictionLabel)
    assert len(labels) >= 2
