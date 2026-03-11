"""Preprocess raw data into train/val/test splits."""

import json
import random
from pathlib import Path

from pipelines.config.reproducibility import set_all_seeds


def preprocess(
    input_path: str = "data/raw",
    output_path: str = "data/processed",
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    seed: int = 42,
) -> None:
    """Load raw data, split into train/val/test, and save."""
    set_all_seeds(seed)

    raw_dir = Path(input_path)
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_data: list[dict] = []  # type: ignore[type-arg]
    for json_file in raw_dir.glob("*.json"):
        with json_file.open() as f:
            data = json.load(f)
            if isinstance(data, list):
                all_data.extend(data)

    if not all_data:
        print(f"No data found in {raw_dir}")
        return

    random.shuffle(all_data)

    n = len(all_data)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    splits = {
        "train": all_data[:train_end],
        "val": all_data[train_end:val_end],
        "test": all_data[val_end:],
    }

    for name, data in splits.items():
        path = out_dir / f"{name}.json"
        with path.open("w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  {name}: {len(data)} samples -> {path}")


if __name__ == "__main__":
    preprocess()
