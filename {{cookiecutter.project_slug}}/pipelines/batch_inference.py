"""Batch inference script for processing data files."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from {{ cookiecutter.project_slug }}.adapters.inbound.dependencies import get_predictor
from {{ cookiecutter.project_slug }}.domain.value_objects.prediction_input import PredictionInput


def batch_predict(
    input_path: str,
    output_path: str,
) -> None:
    """Run predictions on a JSON file of inputs."""
    predictor = get_predictor()

    with Path(input_path).open() as f:
        items = json.load(f)

    results = []
    for i, item in enumerate(items):
        text = item.get("text", "")
        try:
            input_data = PredictionInput(text=text)
            result = predictor.predict(input_data)
            results.append(
                {
                    "text": text,
                    "prediction": result.label.value,
                    "confidence": result.confidence.value,
                }
            )
        except Exception as e:
            results.append({"text": text, "error": str(e)})

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(items)}")

    with Path(output_path).open("w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Batch inference complete: {len(results)} predictions -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m pipelines.batch_inference <input.json> <output.json>")
        sys.exit(1)
    batch_predict(sys.argv[1], sys.argv[2])
