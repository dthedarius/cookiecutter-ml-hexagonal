"""Threshold sweep analysis for finding optimal classification threshold."""


def sweep_thresholds(
    scores: list[float],
    labels: list[int],
    thresholds: list[float] | None = None,
) -> list[dict[str, float]]:
    """Sweep across thresholds and compute metrics at each point."""
    from sklearn.metrics import f1_score, precision_score, recall_score

    if thresholds is None:
        thresholds = [i / 100 for i in range(5, 100, 5)]

    results = []
    for t in thresholds:
        preds = [1 if s >= t else 0 for s in scores]
        results.append(
            {
                "threshold": t,
                "precision": precision_score(labels, preds, zero_division=0),
                "recall": recall_score(labels, preds, zero_division=0),
                "f1": f1_score(labels, preds, zero_division=0),
            }
        )

    return results


def main() -> None:
    """Run threshold analysis on test data."""
    print("Threshold analysis requires model predictions.")
    print("Use `make experiment config=...` for full pipeline including threshold sweep.")


if __name__ == "__main__":
    main()
