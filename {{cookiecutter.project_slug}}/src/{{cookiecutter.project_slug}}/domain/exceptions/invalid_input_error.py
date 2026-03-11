from {{ cookiecutter.project_slug }}.domain.exceptions.prediction_error import PredictionError


class InvalidInputError(PredictionError):
    """Raised when input data fails validation."""
