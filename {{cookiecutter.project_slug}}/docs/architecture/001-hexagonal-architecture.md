# ADR-001: Hexagonal Architecture

## Status

Accepted

## Context

We need a clean architecture for our ML service that:
- Separates business logic from infrastructure
- Makes it easy to swap ML model implementations
- Enables thorough testing without external dependencies
- Supports multiple deployment targets (API, batch, CLI)

## Decision

We adopt hexagonal architecture (ports and adapters):

- **Domain**: Pure business logic, no framework dependencies
- **Ports**: Protocol-based interfaces (Python `typing.Protocol`)
- **Adapters**: Framework-specific implementations (FastAPI, MLflow, model libs)

### Dependency Rule

```
adapters -> ports <- domain
```

Domain knows nothing about the outside world. Adapters implement port protocols.

## Consequences

### Positive
- ML models are swappable via `ModelPort` protocol
- Domain logic is testable without loading real models
- API framework (FastAPI) can be replaced without touching domain
- Clear boundaries prevent spaghetti dependencies

### Negative
- More files and indirection than a flat structure
- Protocol compliance must be manually verified (no runtime check by default)
- New team members need to understand the pattern
