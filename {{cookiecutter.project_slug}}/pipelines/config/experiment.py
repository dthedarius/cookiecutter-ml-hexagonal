"""Experiment configuration with YAML composition by reference."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class ExperimentConfig(BaseModel):
    """Top-level experiment config that references model and training configs."""

    name: str
    description: str = ""
    model: str
    training: str | None = None
    metric_to_optimize: str = "{{ cookiecutter.primary_metric }}"
    target_metric_value: float = {{ cookiecutter.target_metric_value }}

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ExperimentConfig":
        """Load experiment config from YAML, resolving model/training references."""
        config_path = Path(path)
        with config_path.open() as f:
            raw = yaml.safe_load(f)
        return cls(**raw)

    def resolve_model_config(self, configs_dir: str | Path = "configs") -> dict[str, Any]:
        """Resolve model reference to full config dict."""
        model_path = Path(configs_dir) / "model" / f"{self.model}.yaml"
        if model_path.exists():
            with model_path.open() as f:
                return yaml.safe_load(f)
        return {"name": self.model, "type": self.model}

    def resolve_training_config(self, configs_dir: str | Path = "configs") -> dict[str, Any] | None:
        """Resolve training reference to full config dict."""
        if self.training is None:
            return None
        training_path = Path(configs_dir) / "training" / f"{self.training}.yaml"
        if training_path.exists():
            with training_path.open() as f:
                return yaml.safe_load(f)
        return None
