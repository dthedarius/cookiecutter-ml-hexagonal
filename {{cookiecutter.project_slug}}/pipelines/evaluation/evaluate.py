"""Evaluation metrics computation."""

import json
from pathlib import Path


def compute_metrics(
    predictions: list[int],
    labels: list[int],
) -> dict[str, float]:
    """Compute classification metrics."""
    from sklearn.metrics import (
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
    )

    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(labels, predictions, average="weighted", zero_division=0),
        "recall": recall_score(labels, predictions, average="weighted", zero_division=0),
        "f1": f1_score(labels, predictions, average="weighted", zero_division=0),
    }


def evaluate(data_path: str = "data/processed/test.json") -> dict[str, float]:
    """Load test data and evaluate current model."""
    path = Path(data_path)
    if not path.exists():
        print(f"Test data not found at {path}")
        return {}

    with path.open() as f:
        test_data = json.load(f)

    print(f"Evaluating on {len(test_data)} test samples")
    return {}


if __name__ == "__main__":
    metrics = evaluate()
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")
