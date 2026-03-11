"""Baseline model using simple rule-based matching."""

from pathlib import Path
from typing import Any

from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel
from {{ cookiecutter.project_slug }}.ports.outbound.model_port import ModelPort
from {{ cookiecutter.project_slug }}.ports.outbound.trainable_model_port import TrainableModelPort


class BaselineModel:
    """Rule-based baseline model. Always the first model to run as a sanity check."""

    def __init__(self) -> None:
        self._loaded = True

    def predict(self, text: str) -> dict[str, float]:
        """Simple baseline prediction. Override with your own logic."""
        labels = list(PredictionLabel)
        # Default: return equal scores for all labels
        score = 1.0 / len(labels)
        return {label.value: score for label in labels}

    def is_loaded(self) -> bool:
        return self._loaded

    def train(
        self,
        train_data: Any,
        val_data: Any,
        config: Any,
    ) -> dict[str, float]:
        return {}

    def evaluate(self, test_data: list[dict[str, Any]]) -> dict[str, float]:
        """Evaluate on test data. Each item must have 'text' and 'label' keys."""
        if not test_data:
            return {"recall": 0.0, "precision": 0.0, "f1": 0.0}

        labels = list(PredictionLabel)
        correct = 0
        total = len(test_data)

        for item in test_data:
            text = item["text"]
            true_label = item["label"]
            scores = self.predict(text)
            pred_label = max(scores, key=scores.get)  # type: ignore[arg-type]
            if pred_label == true_label or pred_label == labels[int(true_label)].value:
                correct += 1

        accuracy = correct / total if total > 0 else 0.0
        return {"accuracy": accuracy, "f1": accuracy}

    def save(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        (path / "baseline.txt").write_text("baseline-model")

    def load(self, path: Path) -> None:
        pass


def _check_model_protocol() -> None:
    _: ModelPort = BaselineModel()


def _check_trainable_protocol() -> None:
    _: TrainableModelPort = BaselineModel()


_check_model_protocol()
_check_trainable_protocol()
