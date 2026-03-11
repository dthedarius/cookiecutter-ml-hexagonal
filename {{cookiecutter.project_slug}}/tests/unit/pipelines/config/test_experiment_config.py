from pathlib import Path

import yaml
from pipelines.config.experiment import ExperimentConfig


def test_from_yaml(tmp_path: Path) -> None:
    config_data = {
        "name": "test-experiment",
        "description": "Test experiment",
        "model": "baseline",
        "metric_to_optimize": "f1",
        "target_metric_value": 0.9,
    }
    config_file = tmp_path / "test.yaml"
    with config_file.open("w") as f:
        yaml.dump(config_data, f)

    config = ExperimentConfig.from_yaml(config_file)
    assert config.name == "test-experiment"
    assert config.model == "baseline"
    assert config.metric_to_optimize == "f1"


def test_resolve_model_config_from_file(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    model_dir.mkdir()
    model_config = {"name": "baseline", "type": "baseline"}
    with (model_dir / "baseline.yaml").open("w") as f:
        yaml.dump(model_config, f)

    config = ExperimentConfig(name="test", model="baseline")
    resolved = config.resolve_model_config(tmp_path)
    assert resolved["name"] == "baseline"
    assert resolved["type"] == "baseline"


def test_resolve_model_config_fallback() -> None:
    config = ExperimentConfig(name="test", model="nonexistent")
    resolved = config.resolve_model_config("/nonexistent/path")
    assert resolved["name"] == "nonexistent"
    assert resolved["type"] == "nonexistent"


def test_resolve_training_config_none() -> None:
    config = ExperimentConfig(name="test", model="baseline", training=None)
    assert config.resolve_training_config() is None
