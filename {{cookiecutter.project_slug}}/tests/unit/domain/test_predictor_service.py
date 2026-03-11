import pytest

from {{ cookiecutter.project_slug }}.domain.exceptions.model_not_loaded_error import (
    ModelNotLoadedError,
)
from {{ cookiecutter.project_slug }}.domain.services.predictor_service import PredictorService
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_input import PredictionInput
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel


class FakeModel:
    def __init__(self, loaded: bool = True) -> None:
        self._loaded = loaded
        labels = list(PredictionLabel)
        self._scores = {labels[0].value: 0.8}
        for label in labels[1:]:
            self._scores[label.value] = 0.2 / (len(labels) - 1)

    def predict(self, text: str) -> dict[str, float]:
        return self._scores

    def is_loaded(self) -> bool:
        return self._loaded


def test_predict_returns_result() -> None:
    model = FakeModel()
    service = PredictorService(model=model)
    input_data = PredictionInput(text="test input")
    result = service.predict(input_data)
    assert result.label in list(PredictionLabel)
    assert 0.0 <= result.confidence.value <= 1.0


def test_predict_raises_when_model_not_loaded() -> None:
    model = FakeModel(loaded=False)
    service = PredictorService(model=model)
    input_data = PredictionInput(text="test input")
    with pytest.raises(ModelNotLoadedError):
        service.predict(input_data)


def test_is_model_loaded() -> None:
    model = FakeModel(loaded=True)
    service = PredictorService(model=model)
    assert service.is_model_loaded() is True


def test_is_model_not_loaded() -> None:
    model = FakeModel(loaded=False)
    service = PredictorService(model=model)
    assert service.is_model_loaded() is False
