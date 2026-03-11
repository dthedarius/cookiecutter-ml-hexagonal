# {{ cookiecutter.project_name }} — Roadmap

This roadmap covers the full ML project lifecycle from problem understanding to production deployment.
Each phase is designed to be completed sequentially, with clear deliverables and validation criteria.

---

## Phase 1: Problem Understanding & Data Exploration

**Goal:** Understand the problem domain, assess data quality, and define success criteria.

- [ ] Define the business problem and success metrics
- [ ] Collect and inventory raw data in `data/raw/`
- [ ] Run exploratory data analysis (`notebooks/01_exploratory_data_analysis.ipynb`)
  - Data quality assessment (missing values, duplicates, outliers)
  - Target distribution analysis (class imbalance / target range)
  - Feature distributions and correlations
- [ ] Validate data against schemas (`make validate-data`)
- [ ] Document findings and preprocessing decisions

**Validation:** EDA notebook completed, data quality issues documented.

---

## Phase 2: Baseline Model

**Goal:** Establish a performance floor that all future models must beat.

- [ ] Run the rule-based baseline model (`notebooks/02_baseline_model.ipynb`)
- [ ] Record baseline metrics in MLflow (`make experiment config=configs/experiment/baseline.yaml`)
- [ ] Verify baseline via `make compare`
- [ ] Set target metric: `{{ cookiecutter.primary_metric }}` >= `{{ cookiecutter.target_metric_value }}`

**Validation:** Baseline metrics recorded in MLflow, target defined.

---

## Phase 3: Model Development & Experimentation

**Goal:** Iterate on models, features, and hyperparameters to beat the baseline.

- [ ] Implement model adapter in `src/{{ cookiecutter.project_slug }}/adapters/outbound/`
  - Must implement `ModelPort` and `TrainableModelPort` protocols
- [ ] Register new model in `pipelines/run_experiment.py` MODEL_REGISTRY
- [ ] Create experiment config in `configs/experiment/`
- [ ] Train and evaluate (`notebooks/03_model_experiments.ipynb` or `make experiment`)
- [ ] Track all experiments in MLflow (`make mlflow-ui`)
- [ ] Compare runs (`make compare`)
{% if cookiecutter.ml_task != "regression" %}
- [ ] Optimize prediction threshold (`pipelines/evaluation/threshold_analysis.py`)
{% endif %}

**Validation:** At least one model beats the baseline on `{{ cookiecutter.primary_metric }}`.

---

## Phase 4: Testing & Validation

**Goal:** Ensure model quality and code reliability before deployment.

- [ ] Unit tests for domain logic (`make test-unit`)
- [ ] Integration tests for API endpoints (`make test-integration`)
- [ ] Model performance tests (metrics above target on test set)
- [ ] Data validation pipeline (`make validate-data`)
- [ ] Lint and type checks pass (`make check`)

**Validation:** `make check` passes, model meets target metric on held-out test set.

---

## Phase 5: Deployment & CI/CD

**Goal:** Deploy the model as a production service with automated quality gates.

- [ ] Build Docker image (`make docker-build`)
- [ ] Deploy with Docker Compose (`make docker-up`)
  - API at `http://localhost:8000`
  - MLflow at `http://localhost:5000`
- [ ] Verify API endpoints:
  - `POST /predict` — prediction endpoint
  - `GET /health/ready` — readiness probe (model loaded)
  - `GET /health/live` — liveness probe
- [ ] CI pipeline validates on every push (`.github/workflows/ci.yml`)
  - Lint, type check, unit tests, integration tests
- [ ] ML validation gate (`.github/workflows/ml-validation.yml`)
  - Data schema validation, config validation

**Validation:** API responds correctly, CI pipeline green, health checks pass.

---

## Phase 6: Monitoring & Iteration

**Goal:** Monitor model performance in production and iterate.

- [ ] Monitor API metrics (request latency, error rates)
- [ ] Track prediction distribution drift
- [ ] Set up alerts for model degradation
- [ ] Retrain workflow: new data → preprocess → train → evaluate → deploy
- [ ] Version model artifacts in MLflow Model Registry

**Validation:** Monitoring dashboards active, retraining workflow documented.

---

## Agent Orchestration Plan

This section describes how AI agents can autonomously execute the ML lifecycle above.

### Architecture: Orchestrator + Specialized Sub-Agents

```
┌─────────────────────────────────────┐
│         Orchestrator Agent          │
│  (reads ROADMAP, tracks progress)   │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────────┐
    │          │              │
    ▼          ▼              ▼
┌────────┐ ┌────────┐  ┌──────────┐
│  EDA   │ │ Train  │  │  Deploy  │
│ Agent  │ │ Agent  │  │  Agent   │
└────────┘ └────────┘  └──────────┘
```

### Orchestrator Agent

**Role:** Reads this ROADMAP, determines current phase, delegates to sub-agents, and tracks progress.

**Responsibilities:**
- Parse ROADMAP.md to determine which phase/task is next
- Delegate tasks to the appropriate sub-agent
- Validate deliverables after each sub-agent completes
- Update checklist status in ROADMAP.md
- Decide when to move to the next phase

### Sub-Agent 1: EDA Agent

**Scope:** Phase 1 — Problem Understanding & Data Exploration

**Capabilities:**
- Load and profile datasets (summary statistics, distributions)
- Detect data quality issues (missing values, duplicates, outliers)
- Identify problem type (classification vs regression vs clustering)
- Generate visualizations in notebooks
- Write findings to `notebooks/01_exploratory_data_analysis.ipynb`

**Inputs:** Raw data in `data/raw/`
**Outputs:** Completed EDA notebook, data quality report

### Sub-Agent 2: Training Agent

**Scope:** Phases 2–4 — Baseline, Experimentation, Validation

**Capabilities:**
- Generate and preprocess training data (`make generate-data`, `make preprocess`)
- Run baseline experiments (`make experiment config=configs/experiment/baseline.yaml`)
- Implement new model adapters (following `ModelPort` protocol)
- Create experiment configs and run experiments
- Compare MLflow runs and select best model
- Write and run tests (`make test-unit`, `make test-integration`)

**Inputs:** Preprocessed data in `data/processed/`, experiment configs
**Outputs:** Trained model artifacts, MLflow experiment runs, passing tests

### Sub-Agent 3: Deployment Agent

**Scope:** Phases 5–6 — Deployment, Monitoring

**Capabilities:**
- Build and test Docker images
- Verify API endpoints and health checks
- Validate CI/CD pipeline configuration
- Set up monitoring and alerting
- Document deployment runbooks

**Inputs:** Trained model, passing test suite
**Outputs:** Running production service, CI/CD pipeline, monitoring

### Agent Workflow

```
1. Orchestrator reads ROADMAP.md → identifies Phase 1 incomplete
2. Orchestrator delegates to EDA Agent
3. EDA Agent runs notebooks, reports findings
4. Orchestrator validates Phase 1 deliverables → marks complete
5. Orchestrator delegates to Training Agent for Phase 2
6. Training Agent runs baseline, reports metrics
7. Orchestrator checks if baseline meets target → proceeds to Phase 3
8. Training Agent iterates on models until target met
9. Orchestrator validates Phase 4 (testing) → delegates to Deployment Agent
10. Deployment Agent builds, deploys, verifies
11. Orchestrator marks all phases complete
```

### Agent Instructions Location

Each agent reads its instructions from:
- **Orchestrator:** `ROADMAP.md` (this file) + `CLAUDE.md`
- **EDA Agent:** `notebooks/01_exploratory_data_analysis.ipynb` checklist
- **Training Agent:** `CLAUDE.md` (architecture rules) + `configs/` (experiment configs)
- **Deployment Agent:** `docs/runbooks/model-deployment.md` + `Makefile` commands
