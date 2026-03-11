from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_label import PredictionLabel

DEFAULT_THRESHOLD = {{ cookiecutter.prediction_threshold }}


def apply_threshold(
    raw_scores: dict[str, float],
    threshold: float = DEFAULT_THRESHOLD,
) -> PredictionLabel:
    """Apply threshold to raw scores and return the predicted label.

    Returns the label with the highest score above the threshold,
    or the first label if no score exceeds the threshold.
    """
    labels = list(PredictionLabel)
    best_label = labels[0]
    best_score = 0.0

    for label in labels:
        score = raw_scores.get(label.value, 0.0)
        if score > best_score:
            best_score = score
            best_label = label

    return best_label
