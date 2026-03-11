from {{ cookiecutter.project_slug }}.domain.exceptions.model_not_loaded_error import (
    ModelNotLoadedError,
)
from {{ cookiecutter.project_slug }}.domain.services.input_sanitizer import sanitize
from {{ cookiecutter.project_slug }}.domain.services.threshold_service import (
    DEFAULT_THRESHOLD,
    apply_threshold,
)
from {{ cookiecutter.project_slug }}.domain.value_objects.confidence_score import ConfidenceScore
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_input import PredictionInput
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_result import PredictionResult
from {{ cookiecutter.project_slug }}.ports.outbound.model_port import ModelPort


class PredictorService:
    def __init__(
        self,
        model: ModelPort,
        threshold: float = DEFAULT_THRESHOLD,
    ) -> None:
        self._model = model
        self._threshold = threshold

    def is_model_loaded(self) -> bool:
        return self._model.is_loaded()

    def predict(self, input_data: PredictionInput) -> PredictionResult:
        if not self._model.is_loaded():
            raise ModelNotLoadedError("Model is not loaded")

        sanitized_text = sanitize(input_data.text)
        raw_scores = self._model.predict(sanitized_text)
        label = apply_threshold(raw_scores, self._threshold)

        confidence_value = raw_scores.get(label.value, 0.0)

        return PredictionResult(
            label=label,
            confidence=ConfidenceScore(value=confidence_value),
            raw_scores=raw_scores,
        )
