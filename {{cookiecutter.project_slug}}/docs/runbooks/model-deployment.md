# Runbook: Model Deployment

## Prerequisites

- Access to production environment
- Trained model with metrics meeting target threshold
- MLflow tracking URI configured

## Steps

### 1. Verify model metrics

```bash
make compare
```

Ensure the model meets the target: `{{ cookiecutter.primary_metric }} >= {{ cookiecutter.target_metric_value }}`

### 2. Export model artifacts

```bash
make experiment config=configs/experiment/<your-experiment>.yaml
```

### 3. Build Docker image

```bash
make docker-build
```

### 4. Test locally

```bash
make docker-up
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "test input"}'
```

### 5. Deploy

Push Docker image to registry and update deployment configuration.

## Rollback

1. Revert to previous Docker image tag
2. Verify health endpoints respond correctly
3. Run smoke tests against the rolled-back version
