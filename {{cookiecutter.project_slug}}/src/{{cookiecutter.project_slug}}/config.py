"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):  # type: ignore[misc]
    """Application settings loaded from environment variables."""

    # Application
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Model
    prediction_threshold: float = {{ cookiecutter.prediction_threshold }}
    model_type: str = "baseline"
{% if cookiecutter.model_framework == "huggingface" %}
    model_checkpoint: str = "distilbert-base-uncased"
{% endif %}

    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "{{ cookiecutter.project_slug }}"
{% if cookiecutter.include_auth == "api_key" %}

    # Authentication
    api_key: str = ""
{% endif %}

    model_config = {"env_prefix": "", "env_file": ".env", "extra": "ignore"}
