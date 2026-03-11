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

## ML Workflow

Follow the [ROADMAP.md](ROADMAP.md) for the complete project lifecycle.

### 1. Explore Data
{% if cookiecutter.include_notebooks == "yes" %}

```bash
uv sync --extra notebooks
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```
{% endif %}

```bash
make generate-data   # Generate sample data
make validate-data   # Validate data schemas
```

### 2. Train & Evaluate

```bash
make preprocess      # Preprocess raw data into train/val/test splits
make experiment config=configs/experiment/baseline.yaml
make compare         # Compare MLflow runs
make mlflow-ui       # View at http://localhost:5000
```

### 3. Run Full Pipeline

```bash
make pipeline        # generate-data → validate → preprocess → train → evaluate
```

### 4. Deploy

```bash
make docker-build    # Build Docker image
docker compose up -d # API at :8000, MLflow at :5000
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

## Project Structure

See [CLAUDE.md](CLAUDE.md) for full architecture documentation.

## Development

See [docs/contributing.md](docs/contributing.md) for development workflow.
