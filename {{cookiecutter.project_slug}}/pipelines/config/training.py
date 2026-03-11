from pydantic import BaseModel


class TrainingConfig(BaseModel):
    epochs: int = 5
    batch_size: int = 16
    learning_rate: float = 2e-5
    weight_decay: float = 0.01
    max_length: int = 256
    eval_strategy: str = "epoch"
    seed: int = 42
