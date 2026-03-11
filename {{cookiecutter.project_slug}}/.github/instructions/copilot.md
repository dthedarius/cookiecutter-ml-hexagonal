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

## Agent Orchestration

This project uses a multi-agent system for autonomous ML lifecycle execution.
See the dedicated instruction files for each agent:

- **Orchestrator:** [`.github/instructions/orchestrator.md`](orchestrator.md) — Main coordinator with iteration limits and phase management
- **EDA Agent:** [`.github/instructions/eda-agent.md`](eda-agent.md) — Data exploration (max 3 iterations)
- **Training Agent:** [`.github/instructions/training-agent.md`](training-agent.md) — Model training and validation (max 5 iterations)
- **Deployment Agent:** [`.github/instructions/deployment-agent.md`](deployment-agent.md) — Build, deploy, and verify (max 3 iterations)

### Key Rules for All Agents

1. **Iteration limits are hard constraints** — never exceed them
2. **Every sub-agent has strict success metrics** — validated by the orchestrator
3. **Early stop on success** — if the target metric is met, stop iterating
4. **Scientific method** — every experiment must have a hypothesis, test, and conclusion
5. **No infinite loops** — max iterations + per-hypothesis limits prevent runaway execution
