"""Input sanitization for security - defense in depth."""

import re


def sanitize(text: str) -> str:
    """Sanitize input text by removing potentially dangerous content.

    This is a defense-in-depth measure. Input validation happens at the
    value object level (PredictionInput); this handles content-level sanitization.
    """
    # Remove null bytes
    text = text.replace("\x00", "")

    # Normalize whitespace (collapse multiple spaces/newlines)
    text = re.sub(r"\s+", " ", text).strip()

    return text
