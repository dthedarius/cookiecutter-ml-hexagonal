from pydantic import BaseModel


class ModelConfig(BaseModel):
    name: str
    type: str
    checkpoint: str | None = None
    label_map: dict[str, str] | None = None
