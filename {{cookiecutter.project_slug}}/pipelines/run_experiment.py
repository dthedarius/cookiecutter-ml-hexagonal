"""Experiment orchestrator with generic model registry."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.config.experiment import ExperimentConfig
from pipelines.config.model import ModelConfig
from pipelines.config.reproducibility import set_all_seeds
from pipelines.config.training import TrainingConfig

from {{ cookiecutter.project_slug }}.adapters.outbound.baseline_model import BaselineModel

# Model registry: maps model type names to adapter classes
MODEL_REGISTRY: dict[str, type] = {
    "baseline": BaselineModel,
}


def load_data(data_dir: str = "data/processed") -> tuple[Any, Any, Any]:
    """Load train/val/test data splits."""
    data_path = Path(data_dir)

    train_path = data_path / "train.json"
    val_path = data_path / "val.json"
    test_path = data_path / "test.json"

    if not train_path.exists():
        print(f"No processed data found at {data_path}. Run preprocessing first.")
        sys.exit(1)

    with train_path.open() as f:
        train_data = json.load(f)
    with val_path.open() as f:
        val_data = json.load(f)
    with test_path.open() as f:
        test_data = json.load(f)

    return train_data, val_data, test_data


def run_experiment(config_path: str) -> None:
    """Run a single experiment from a YAML config file."""
    experiment = ExperimentConfig.from_yaml(config_path)
    model_config_dict = experiment.resolve_model_config()
    model_config = ModelConfig(**model_config_dict)

    print(f"\n{'='*60}")
    print(f"Experiment: {experiment.name}")
    print(f"Model: {model_config.name} (type={model_config.type})")
    print(f"Metric: {experiment.metric_to_optimize} >= {experiment.target_metric_value}")
    print(f"{'='*60}\n")

    # Resolve training config
    training_config = None
    if experiment.training:
        training_dict = experiment.resolve_training_config()
        if training_dict:
            training_config = TrainingConfig(**training_dict)

    # Set seeds for reproducibility
    seed = training_config.seed if training_config else 42
    set_all_seeds(seed)

    # Instantiate model from registry
    model_type = model_config.type
    if model_type not in MODEL_REGISTRY:
        print(f"Unknown model type: {model_type}. Available: {list(MODEL_REGISTRY.keys())}")
        sys.exit(1)

    model_cls = MODEL_REGISTRY[model_type]
    model = model_cls()

    # Start MLflow tracking
    try:
        import mlflow

        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment("{{ cookiecutter.project_slug }}")

        with mlflow.start_run(run_name=experiment.name):
            mlflow.log_params(
                {
                    "experiment_name": experiment.name,
                    "model_type": model_config.type,
                    "model_name": model_config.name,
                    "seed": seed,
                }
            )

            if training_config:
                mlflow.log_params(
                    {
                        "epochs": training_config.epochs,
                        "batch_size": training_config.batch_size,
                        "learning_rate": training_config.learning_rate,
                    }
                )

            # Load data and run training if applicable
            if training_config and hasattr(model, "train"):
                train_data, val_data, test_data = load_data()
                print("Training model...")
                train_metrics = model.train(train_data, val_data, training_config)
                for k, v in train_metrics.items():
                    mlflow.log_metric(f"train_{k}", v)
            else:
                _, _, test_data = load_data()

            # Evaluate
            print("Evaluating model...")
            eval_metrics = model.evaluate(test_data)
            for k, v in eval_metrics.items():
                mlflow.log_metric(k, v)
                print(f"  {k}: {v:.4f}")

            # Check target metric
            target_value = eval_metrics.get(experiment.metric_to_optimize, 0.0)
            met_target = target_value >= experiment.target_metric_value
            mlflow.log_metric("met_target", float(met_target))

            if met_target:
                print(
                    f"\n Target met: {experiment.metric_to_optimize}="
                    f"{target_value:.4f} >= {experiment.target_metric_value}"
                )
            else:
                print(
                    f"\n Target NOT met: {experiment.metric_to_optimize}="
                    f"{target_value:.4f} < {experiment.target_metric_value}"
                )

            # Save model
            model_path = Path("models") / experiment.name
            if hasattr(model, "save"):
                model.save(model_path)
                mlflow.log_artifacts(str(model_path))
                print(f"Model saved to {model_path}")

    except ImportError:
        print("MLflow not available. Running without tracking.")
        _, _, test_data = load_data()
        eval_metrics = model.evaluate(test_data)
        for k, v in eval_metrics.items():
            print(f"  {k}: {v:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ML experiment")
    parser.add_argument("--config", required=True, help="Path to experiment YAML config")
    args = parser.parse_args()
    run_experiment(args.config)


if __name__ == "__main__":
    main()
