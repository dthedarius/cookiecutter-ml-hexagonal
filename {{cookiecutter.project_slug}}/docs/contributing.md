# Contributing to {{ cookiecutter.project_name }}

## Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd {{ cookiecutter.project_slug }}

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Verify setup
make check
```

## Development Workflow

### 1. Create a branch

```bash
git checkout -b feat/<short-name>
```

### 2. Follow TDD

1. Write a failing test
2. Write minimum code to pass
3. Refactor while keeping tests green

### 3. Verify

```bash
make check  # lint + typecheck + unit tests
```

### 4. Create a Pull Request

- Fill in the PR template
- Ensure CI passes
- Request review

## Architecture Rules

- **Domain layer** has ZERO external imports (except pydantic)
- **Ports** use `typing.Protocol` only
- **Adapters** must implement port Protocols
- Tests mirror the source structure

## Code Style

- Managed by `ruff` (linting + formatting)
- Type annotations required on all public functions
- One class per file for entities, value objects, protocols
