from typing import Protocol

from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_input import PredictionInput
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_result import PredictionResult


class PredictPort(Protocol):
    def predict(self, input_data: PredictionInput) -> PredictionResult: ...
