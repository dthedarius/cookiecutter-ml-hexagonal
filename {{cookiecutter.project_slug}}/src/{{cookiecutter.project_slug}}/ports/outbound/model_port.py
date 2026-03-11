from typing import Protocol


class ModelPort(Protocol):
    def predict(self, text: str) -> dict[str, float]: ...

    def is_loaded(self) -> bool: ...
