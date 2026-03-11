"""Training script - delegates to model adapter's train method."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipelines.config.reproducibility import set_all_seeds
from pipelines.config.training import TrainingConfig


def train(
    data_dir: str = "data/processed",
    config: TrainingConfig | None = None,
) -> dict[str, float]:
    """Train model using processed data."""
    if config is None:
        config = TrainingConfig()

    set_all_seeds(config.seed)

    data_path = Path(data_dir)
    with (data_path / "train.json").open() as f:
        train_data = json.load(f)
    with (data_path / "val.json").open() as f:
        val_data = json.load(f)

    print(f"Training with {len(train_data)} train, {len(val_data)} val samples")
    print(f"Config: epochs={config.epochs}, lr={config.learning_rate}, batch={config.batch_size}")
    print("Use `make experiment config=...` for full training pipeline.")
    return {}


if __name__ == "__main__":
    train()
