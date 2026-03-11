# {{ cookiecutter.project_name }} - Project Guidelines

## Project

{{ cookiecutter.project_description }}

## Architecture: Hexagonal (Ports & Adapters)

### Layer Rules
- **`domain/`** -- Pure business logic. ZERO imports from `adapters/`, frameworks (FastAPI, etc.), or external libraries (except `pydantic` for value objects).
- **`ports/`** -- Interface definitions using `typing.Protocol` only. No implementations.
- **`adapters/`** -- Framework-specific implementations. Must implement port Protocols. Dependency injection required.
- **Dependency direction:** `adapters -> ports <- domain` (adapters depend on ports; domain depends on nothing external)
- **`pipelines/`** -- ML tooling (data generation, training, evaluation). Outside hexagonal architecture -- not runtime code.

### File Constraints
- Tests mirror source: `src/{{ cookiecutter.project_slug }}/domain/services/predictor_service.py` -> `tests/unit/domain/test_predictor_service.py`
- One class per file (entities, value objects, protocols)
- All public functions and methods must have type annotations

## TDD Workflow
1. **RED** -- Write a failing test first
2. **GREEN** -- Write minimum code to make it pass
3. **REFACTOR** -- Clean up while keeping tests green

## Commands (always use `uv`)
```bash
uv sync                          # Install dependencies
uv run pytest tests/ -v          # Run all tests
uv run pytest tests/unit/ -v     # Run unit tests only
uv run ruff check src/ tests/    # Lint
uv run ruff format src/ tests/   # Format
uv run mypy src/                 # Type check
make check                       # Lint + typecheck + unit tests
make serve                       # API FastAPI (port 8000)
make generate-data               # Generate sample data
make validate-data               # Validate data against schemas
make preprocess                  # Tokenize and split data
make train                       # Train model
make evaluate                    # Evaluate performance
make mlflow-ui                   # MLflow UI (port 5000)
make experiment config=configs/experiment/<name>.yaml  # Run experiment
make experiment-all              # Run all experiments
make compare                     # Compare MLflow runs
```

## Package Structure
```
src/{{ cookiecutter.project_slug }}/
|-- config.py                    # Pydantic Settings
|-- domain/
|   |-- value_objects/           # PredictionInput, PredictionLabel, ConfidenceScore, PredictionResult
|   |-- services/                # PredictorService, ThresholdService, InputSanitizer
|   +-- exceptions/              # PredictionError, ModelNotLoadedError, InvalidInputError
|-- ports/
|   |-- inbound/                 # PredictPort, HealthCheckPort
|   +-- outbound/                # ModelPort, TrainableModelPort, ExperimentTrackerPort
+-- adapters/
    |-- inbound/                 # FastAPI (api.py, dependencies.py, middleware/)
    +-- outbound/                # BaselineModel, MLflow tracker

pipelines/                       # Outside hexagonal architecture -- ML tooling
|-- config/                      # Pydantic configs (ExperimentConfig, ModelConfig, TrainingConfig)
|-- data_generation/             # Data generation scripts
|-- data_validation/             # Data schema validation
|-- training/                    # Preprocessing + training
|-- evaluation/                  # Metrics, threshold analysis, compare runs
+-- run_experiment.py            # Experiment orchestrator

configs/                         # YAML configs
|-- experiment/                  # Experiment definitions
|-- model/                       # Model configurations
|-- training/                    # Hyperparameters
+-- environments/                # Environment-specific configs
```

## ML Conventions
- Model artifacts gitignored (`models/`, `*.pt`, `*.bin`, `*.safetensors`)
- Generated/processed data gitignored (`data/generated/`, `data/processed/`)
- Threshold configurable via env var `PREDICTION_THRESHOLD` (default: {{ cookiecutter.prediction_threshold }})
- Primary metric: `{{ cookiecutter.primary_metric }}` (target >= {{ cookiecutter.target_metric_value }})

## Experiment Framework
- Configs YAML in `configs/` -- composition by reference (experiment -> model + training)
- Model registry in `pipelines/run_experiment.py`
- All experiments compared against baseline (`make compare`)
- `TrainableModelPort`: interface for trainable models (train/evaluate/save/load)
- `BaselineModel`: rule-based baseline, always run first

## API Endpoints
- `POST /predict` -- `{"text": "input"}` -> `{"prediction": "label", "confidence": 0.95}`
- `GET /health/ready` -- Readiness probe (model loaded)
- `GET /health/live` -- Liveness probe (service up)

## Branching
- **Never push directly to `main`**
- Create branch from `main`:
  - Bug: `fix/<short-name>`
  - Feature: `feat/<short-name>`
  - Refactor/chore: `chore/<short-name>`
- Merge to `main` via Pull Request only

## Core Principles
- **Simplicity First**: Make every change as simple as possible
- **No Laziness**: Find root causes. No temporary fixes
- **Minimal Impact**: Changes should only touch what's necessary
