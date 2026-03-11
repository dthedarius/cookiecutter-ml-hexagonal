import os
from functools import lru_cache

from {{ cookiecutter.project_slug }}.adapters.outbound.baseline_model import BaselineModel
from {{ cookiecutter.project_slug }}.domain.services.predictor_service import PredictorService
from {{ cookiecutter.project_slug }}.domain.services.threshold_service import DEFAULT_THRESHOLD


def _get_threshold() -> float:
    return float(os.environ.get("PREDICTION_THRESHOLD", str(DEFAULT_THRESHOLD)))


@lru_cache(maxsize=1)
def get_predictor() -> PredictorService:
    model = BaselineModel()
    return PredictorService(model=model, threshold=_get_threshold())
