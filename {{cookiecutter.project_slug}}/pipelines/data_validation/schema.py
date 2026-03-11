"""Data validation schemas using Pydantic."""

from pydantic import BaseModel, field_validator

{% if cookiecutter.ml_task == "regression" %}

class DataSample(BaseModel):
    """Schema for a single data sample."""

    text: str
    target: float

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            msg = "Text field must not be empty"
            raise ValueError(msg)
        return v
{% else %}

class DataSample(BaseModel):
    """Schema for a single data sample."""

    text: str
    label: int

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            msg = "Text field must not be empty"
            raise ValueError(msg)
        return v

    @field_validator("label")
    @classmethod
    def label_must_be_valid(cls, v: int) -> int:
        if v not in (0, 1):
            msg = f"Label must be 0 or 1, got {v}"
            raise ValueError(msg)
        return v
{% endif %}
