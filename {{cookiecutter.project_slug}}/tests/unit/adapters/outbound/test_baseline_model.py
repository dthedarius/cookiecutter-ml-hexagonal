from {{ cookiecutter.project_slug }}.adapters.outbound.baseline_model import BaselineModel
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel


def test_baseline_model_is_loaded() -> None:
    model = BaselineModel()
    assert model.is_loaded() is True


def test_baseline_model_predict_returns_scores() -> None:
    model = BaselineModel()
    scores = model.predict("test text")
    labels = list(PredictionLabel)
    for label in labels:
        assert label.value in scores
        assert 0.0 <= scores[label.value] <= 1.0


def test_baseline_model_evaluate_empty_data() -> None:
    model = BaselineModel()
    metrics = model.evaluate([])
    assert metrics["f1"] == 0.0


def test_baseline_model_save_and_load(tmp_path) -> None:  # type: ignore[no-untyped-def]
    model = BaselineModel()
    model.save(tmp_path / "model")
    assert (tmp_path / "model" / "baseline.txt").exists()

    model.load(tmp_path / "model")
    assert model.is_loaded()
