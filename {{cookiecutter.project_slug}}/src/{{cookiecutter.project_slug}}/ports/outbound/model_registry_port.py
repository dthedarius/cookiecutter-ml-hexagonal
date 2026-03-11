from typing import Any, Protocol


class ModelRegistryPort(Protocol):
    """Port for model registry operations (e.g., MLflow Model Registry)."""

    def register_model(self, model_uri: str, name: str) -> Any: ...

    def get_latest_version(self, name: str) -> str: ...

    def transition_stage(self, name: str, version: str, stage: str) -> None: ...
