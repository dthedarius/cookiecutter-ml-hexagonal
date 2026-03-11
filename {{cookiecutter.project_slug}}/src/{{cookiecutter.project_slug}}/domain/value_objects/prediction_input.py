from pydantic import BaseModel, field_validator

MAX_INPUT_LENGTH = 5000


class PredictionInput(BaseModel, frozen=True):
    text: str

    @field_validator("text")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            msg = "Input text must not be empty"
            raise ValueError(msg)
        if len(stripped) > MAX_INPUT_LENGTH:
            msg = f"Input text must not exceed {MAX_INPUT_LENGTH} characters"
            raise ValueError(msg)
        return stripped
