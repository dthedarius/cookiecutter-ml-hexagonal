from pathlib import Path
from typing import Any

from {{ cookiecutter.project_slug }}.ports.outbound.experiment_tracker_port import (
    ExperimentTrackerPort,
)

EXPERIMENT_NAME = "{{ cookiecutter.project_slug }}"


class MlflowTracker:
    def __init__(self, tracking_uri: str = "http://localhost:5000") -> None:
        import mlflow

        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(EXPERIMENT_NAME)
        self._mlflow = mlflow

    def log_metric(self, key: str, value: float) -> None:
        self._mlflow.log_metric(key, value)

    def log_params(self, params: dict[str, Any]) -> None:
        self._mlflow.log_params(params)

    def log_experiment_config(self, config: dict[str, Any]) -> None:
        """Log a flattened experiment config as MLflow params."""
        str_params = {k: str(v) for k, v in config.items()}
        self._mlflow.log_params(str_params)

    def log_model_artifact(self, path: Path) -> None:
        """Log a model directory as an MLflow artifact."""
        self._mlflow.log_artifacts(str(path))


def _check_protocol_compliance() -> None:
    _: ExperimentTrackerPort = MlflowTracker()
