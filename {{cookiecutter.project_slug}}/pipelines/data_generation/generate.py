"""Data generation placeholder script."""

import json
from pathlib import Path


def generate_sample_data(
    output_path: str = "data/raw/sample.json",
    n_samples: int = 100,
) -> None:
    """Generate sample training data for development."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

{% if cookiecutter.ml_task == "regression" %}
    import random

    samples = [
        {"text": f"Sample text {i}", "target": round(random.uniform(0, 1), 3)}
        for i in range(n_samples)
    ]
{% else %}
    samples = [
        {"text": f"Sample text {i}", "label": i % 2}
        for i in range(n_samples)
    ]
{% endif %}

    with path.open("w") as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)

    print(f"Generated {n_samples} samples -> {path}")


if __name__ == "__main__":
    generate_sample_data()
