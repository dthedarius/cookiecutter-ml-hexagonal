# cookiecutter-ml-hexagonal

A production-grade ML project template using hexagonal architecture, TDD, and modern Python tooling.

## Features

- **Hexagonal Architecture** -- Clean separation of domain, ports, and adapters
- **TDD-ready** -- Test structure mirrors source, pre-configured pytest
- **ML Pipeline** -- Experiment orchestrator, model registry, evaluation suite
- **FastAPI** -- REST API with health checks, dependency injection
- **MLflow** -- Experiment tracking and model registry
- **Modern Python** -- uv, ruff, mypy, pre-commit, Python 3.12+
- **Docker** -- Multi-stage build, docker-compose with MLflow
- **CI/CD** -- GitHub Actions with ML validation gate

## Usage

```bash
pip install cookiecutter
cookiecutter cookiecutter-ml-hexagonal/
```

## Template Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `project_name` | My ML Project | Human-readable project name |
| `project_slug` | (auto) | Python package name |
| `ml_task` | text_classification | ML task type |
| `model_framework` | huggingface | Model framework |
| `serving_type` | rest | API type (rest or rest_with_batch) |
| `include_notebooks` | no | Include Jupyter notebooks |
| `include_auth` | none | API authentication |
| `include_monitoring` | basic | Monitoring level |
| `prediction_threshold` | 0.5 | Default prediction threshold |
| `primary_metric` | f1 | Primary evaluation metric |
| `target_metric_value` | 0.90 | Target for primary metric |

## After Generation

```bash
cd your_project
make check    # Verify everything works
make serve    # Start the API
```

## License

MIT
