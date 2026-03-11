from pydantic import BaseModel

from {{ cookiecutter.project_slug }}.domain.value_objects.confidence_score import ConfidenceScore
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel


class PredictionResult(BaseModel, frozen=True):
    label: PredictionLabel
    confidence: ConfidenceScore
    raw_scores: dict[str, float]
    metadata: dict[str, object] = {}
