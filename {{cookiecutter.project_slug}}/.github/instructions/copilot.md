# AI Copilot Instructions for {{ cookiecutter.project_name }}

## Architecture

This project uses hexagonal architecture. Follow these rules strictly:

1. **Domain layer** (`src/{{ cookiecutter.project_slug }}/domain/`) has ZERO external imports except pydantic
2. **Ports** (`src/{{ cookiecutter.project_slug }}/ports/`) define interfaces with `typing.Protocol`
3. **Adapters** (`src/{{ cookiecutter.project_slug }}/adapters/`) implement ports with real dependencies

## Testing

Follow TDD: RED -> GREEN -> REFACTOR. Tests mirror the source structure.

## Key Conventions

- All public functions must have type annotations
- One class per file for value objects, entities, protocols
- Use `uv` for all Python commands
- Run `make check` before committing
