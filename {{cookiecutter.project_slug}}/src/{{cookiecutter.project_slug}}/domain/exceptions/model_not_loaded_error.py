from {{ cookiecutter.project_slug }}.domain.exceptions.prediction_error import PredictionError


class ModelNotLoadedError(PredictionError):
    """Raised when attempting to predict with an unloaded model."""
