from {{ cookiecutter.project_slug }}.domain.services.input_sanitizer import sanitize


def test_sanitize_removes_null_bytes() -> None:
    assert sanitize("hello\x00world") == "helloworld"


def test_sanitize_normalizes_whitespace() -> None:
    assert sanitize("hello   world") == "hello world"


def test_sanitize_strips() -> None:
    assert sanitize("  hello  ") == "hello"


def test_sanitize_collapses_newlines() -> None:
    assert sanitize("hello\n\nworld") == "hello world"
