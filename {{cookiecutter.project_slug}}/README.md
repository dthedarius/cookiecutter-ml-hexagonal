# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Quick Start

```bash
# Install dependencies
uv sync

# Run checks
make check

# Start the API
make serve
```

## API

```bash
# Predict
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "your input text"}'

# Health check
curl http://localhost:8000/health/ready
```

## ML Pipeline

```bash
# Generate sample data
make generate-data

# Validate data
make validate-data

# Run an experiment
make experiment config=configs/experiment/baseline.yaml

# Compare runs
make compare

# MLflow UI
make mlflow-ui
```

## Docker

```bash
docker compose up -d
# API at http://localhost:8000
# MLflow at http://localhost:5000
```

## Project Structure

See [CLAUDE.md](CLAUDE.md) for full architecture documentation.

## Development

See [docs/contributing.md](docs/contributing.md) for development workflow.
