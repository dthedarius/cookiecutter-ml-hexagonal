from typing import Protocol


class HealthCheckPort(Protocol):
    def is_healthy(self) -> bool: ...
