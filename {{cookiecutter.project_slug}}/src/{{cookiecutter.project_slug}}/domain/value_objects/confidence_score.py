from pydantic import BaseModel, field_validator


class ConfidenceScore(BaseModel, frozen=True):
    value: float

    @field_validator("value")
    @classmethod
    def must_be_between_zero_and_one(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            msg = f"Confidence score must be between 0.0 and 1.0, got {v}"
            raise ValueError(msg)
        return v
