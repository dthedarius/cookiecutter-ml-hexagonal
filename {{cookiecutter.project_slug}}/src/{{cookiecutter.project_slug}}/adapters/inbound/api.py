from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

from {{ cookiecutter.project_slug }}.adapters.inbound.dependencies import get_predictor
from {{ cookiecutter.project_slug }}.adapters.inbound.middleware.logging_middleware import (
    LoggingMiddleware,
)
from {{ cookiecutter.project_slug }}.adapters.inbound.middleware.request_id import (
    RequestIdMiddleware,
)
from {{ cookiecutter.project_slug }}.domain.services.predictor_service import PredictorService
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_input import PredictionInput

app = FastAPI(title="{{ cookiecutter.project_name }}", version="0.1.0")

# Middleware (order matters: outermost first)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIdMiddleware)
{% if cookiecutter.include_auth == "api_key" %}
from {{ cookiecutter.project_slug }}.adapters.inbound.middleware.auth import ApiKeyMiddleware  # noqa: E402

app.add_middleware(ApiKeyMiddleware)
{% endif %}


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    raw_scores: dict[str, float] = {}


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


{% if cookiecutter.serving_type == "rest_with_batch" %}
class BatchPredictRequest(BaseModel):
    items: list[PredictRequest]


class BatchPredictResponse(BaseModel):
    predictions: list[PredictResponse]
{% endif %}


@app.post("/predict", response_model=PredictResponse)
def predict(
    request: PredictRequest,
    predictor: PredictorService = Depends(get_predictor),  # noqa: B008
) -> PredictResponse:
    try:
        input_data = PredictionInput(text=request.text)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    result = predictor.predict(input_data)
    return PredictResponse(
        prediction=result.label.value,
        confidence=result.confidence.value,
        raw_scores=result.raw_scores,
    )


{% if cookiecutter.serving_type == "rest_with_batch" %}
@app.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(
    request: BatchPredictRequest,
    predictor: PredictorService = Depends(get_predictor),  # noqa: B008
) -> BatchPredictResponse:
    predictions = []
    for item in request.items:
        try:
            input_data = PredictionInput(text=item.text)
            result = predictor.predict(input_data)
            predictions.append(
                PredictResponse(
                    prediction=result.label.value,
                    confidence=result.confidence.value,
                    raw_scores=result.raw_scores,
                )
            )
        except (ValidationError, Exception):
            predictions.append(
                PredictResponse(prediction="error", confidence=0.0, raw_scores={})
            )
    return BatchPredictResponse(predictions=predictions)
{% endif %}


@app.get("/health/ready", response_model=HealthResponse)
def health_ready(
    predictor: PredictorService = Depends(get_predictor),  # noqa: B008
) -> HealthResponse:
    """Readiness probe - checks if model is loaded and ready to serve."""
    model_loaded = predictor.is_model_loaded()
    return HealthResponse(
        status="ready" if model_loaded else "not_ready",
        model_loaded=model_loaded,
    )


@app.get("/health/live", response_model=HealthResponse)
def health_live() -> HealthResponse:
    """Liveness probe - checks if the service is running."""
    return HealthResponse(status="alive", model_loaded=True)
