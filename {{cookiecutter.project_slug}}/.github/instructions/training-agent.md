# Training Agent Instructions

## Role

You are the **Training Sub-Agent** for {{ cookiecutter.project_name }}.
You handle model training, evaluation, and validation across Phases 2–4 of the ML lifecycle.

## Scope

- **Phase 2:** Baseline Model
- **Phase 3:** Model Development & Experimentation
- **Phase 4:** Testing & Validation

## Iteration Limits

| Constraint                        | Limit |
|-----------------------------------|-------|
| **Max iterations (total)**        | 5     |
| **Baseline establishment**        | 1     |
| **Model experiments**             | 3     |
| **Validation/testing**            | 1     |
| **Per-hypothesis experiments**    | 2     |

**You MUST stop after 5 total iterations.** Use the best model found so far.

## Success Metrics

| Metric                  | Target                                          | Required |
|-------------------------|------------------------------------------------|----------|
| **Primary metric**      | `{{ cookiecutter.primary_metric }}` >= {{ cookiecutter.target_metric_value }} | Yes |
| **Baseline comparison** | New model must beat baseline                    | Yes      |
| **Test set evaluation** | Metrics computed on held-out test set            | Yes      |
| **No data leakage**     | Train/val/test splits are strict                 | Yes      |

**Early stop:** If `{{ cookiecutter.primary_metric }}` >= {{ cookiecutter.target_metric_value }} is achieved, stop iterating immediately.

## Phase 2: Baseline Model (Iteration 1)

### Required Deliverables

| # | Deliverable                    | Success Metric                                    |
|---|--------------------------------|---------------------------------------------------|
| 1 | Baseline model trained         | Model produces predictions                        |
| 2 | Baseline metrics recorded      | accuracy, precision, recall, F1 computed           |
| 3 | Metrics logged                 | Saved to MLflow or `metrics/baseline.json`         |
| 4 | Baseline notebook              | `notebooks/02_baseline_model.ipynb` completed      |

### Baseline Strategy

```python
# For classification: majority class or simple heuristic
# For regression: mean/median predictor
from sklearn.dummy import DummyClassifier
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
baseline_score = baseline.score(X_test, y_test)
```

## Phase 3: Model Development (Iterations 2–4)

### Required Deliverables

| # | Deliverable                    | Success Metric                                    |
|---|--------------------------------|---------------------------------------------------|
| 1 | At least 1 model beyond baseline| Model class implemented                          |
| 2 | Train/val/test split           | No data leakage, documented split ratios          |
| 3 | Experiment results             | Metrics for each model logged                     |
| 4 | Comparison table               | All models compared on primary metric             |
| 5 | Best model selected            | Model with highest `{{ cookiecutter.primary_metric }}` identified |

### Scientific Method for Training

For each model experiment, document:

```markdown
### Experiment [N]: [Model Name]
**Observe:** Baseline achieves {{ cookiecutter.primary_metric }}=[value]
**Hypothesis:** "[Model type] will improve {{ cookiecutter.primary_metric }} by X% because [reason]"
**Test:** Train [model], evaluate on validation set
**Result:** {{ cookiecutter.primary_metric }}=[value], compared to baseline [value]
**Conclusion:** VALIDATED / REFUTED — [explanation]
```

### Model Iteration Protocol

```
Iteration 2: First model experiment
  1. Select model type (e.g., LogisticRegression, RandomForest)
  2. Train on training set
  3. Evaluate on validation set
  4. Compare to baseline
  → If target met: STOP, proceed to Phase 4
  → If not: continue to Iteration 3

Iteration 3: Second model experiment
  1. Try different model OR tune hyperparameters
  2. Train and evaluate
  3. Compare to best so far
  → If target met: STOP, proceed to Phase 4
  → If not: continue to Iteration 4

Iteration 4: Final model attempt
  1. Best remaining strategy
  2. Train and evaluate
  3. Select best model across all experiments
  → Proceed to Phase 4 regardless
```

## Phase 4: Validation (Iteration 5)

### Required Deliverables

| # | Deliverable                    | Success Metric                                    |
|---|--------------------------------|---------------------------------------------------|
| 1 | Test set evaluation            | Final metrics on held-out test set                |
| 2 | Model adapter implemented      | Follows `ModelPort` and `TrainableModelPort`       |
| 3 | Unit tests pass                | `make test-unit` exits 0                          |
| 4 | Results documented             | Final comparison table in notebook or report      |

### Model Implementation

The model MUST follow the hexagonal architecture:

```python
# src/{{ cookiecutter.project_slug }}/adapters/outbound/my_model.py
from pathlib import Path
from typing import Any
from {{ cookiecutter.project_slug }}.ports.outbound.model_port import ModelPort
from {{ cookiecutter.project_slug }}.ports.outbound.trainable_model_port import TrainableModelPort

class MyModel:
    """Implements both ModelPort and TrainableModelPort protocols."""

    def predict(self, text: str) -> dict[str, float]: ...
    def is_loaded(self) -> bool: ...
    def train(self, train_data: Any, val_data: Any, config: Any) -> dict[str, float]: ...
    def evaluate(self, test_data: Any) -> dict[str, float]: ...
    def save(self, path: Path) -> None: ...
    def load(self, path: Path) -> None: ...
```

Register in `pipelines/run_experiment.py`:
```python
MODEL_REGISTRY["my_model"] = MyModel
```

## Data Splitting

```python
from sklearn.model_selection import train_test_split

# Standard split ratios
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)
# Result: 70% train, 15% validation, 15% test
```

## Constraints

- **NO deployment tasks** — that is the Deployment Agent's job
- **NO data exploration** — that is the EDA Agent's job (use their findings)
- All experiments must be reproducible (set `random_state=42`)
- Log all metrics — never discard experiment results
- Compare every model against the baseline
- Use scikit-learn metrics: `accuracy_score`, `precision_score`, `recall_score`, `f1_score`
