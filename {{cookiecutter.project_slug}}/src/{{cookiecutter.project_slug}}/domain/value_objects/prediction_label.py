from enum import Enum

{% if cookiecutter.ml_task == "text_classification" %}
class PredictionLabel(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
{% elif cookiecutter.ml_task == "regression" %}
class PredictionLabel(Enum):
    """For regression tasks, labels represent discretized buckets."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
{% else %}
class PredictionLabel(Enum):
    """Define your custom labels here."""

    CLASS_A = "class_a"
    CLASS_B = "class_b"
{% endif %}
