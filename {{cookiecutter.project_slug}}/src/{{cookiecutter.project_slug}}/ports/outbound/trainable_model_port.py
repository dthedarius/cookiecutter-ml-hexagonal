"""Port for models that support training, evaluation, and persistence."""

from pathlib import Path
from typing import Any, Protocol


class TrainableModelPort(Protocol):
    def train(
        self,
        train_data: Any,
        val_data: Any,
        config: Any,
    ) -> dict[str, float]: ...

    def evaluate(self, test_data: Any) -> dict[str, float]: ...

    def save(self, path: Path) -> None: ...

    def load(self, path: Path) -> None: ...
