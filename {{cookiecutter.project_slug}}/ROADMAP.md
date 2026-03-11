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
Each agent follows the **scientific method**: form a hypothesis, test it, and iterate until validated.

### Architecture: Orchestrator + Specialized Sub-Agents

```
┌──────────────────────────────────────────┐
│           Orchestrator Agent             │
│  (reads ROADMAP, tracks progress,        │
│   enforces hypothesis-driven iteration)  │
└──────────────┬───────────────────────────┘
               │
    ┌──────────┼──────────────┐
    │          │              │
    ▼          ▼              ▼
┌────────┐ ┌────────┐  ┌──────────┐
│  EDA   │ │ Train  │  │  Deploy  │
│ Agent  │ │ Agent  │  │  Agent   │
└────────┘ └────────┘  └──────────┘
```

### Scientific Method Loop

Every sub-agent follows the same iterative loop. The orchestrator enforces this cycle
and decides when enough hypotheses have been validated to move to the next phase.

```
  ┌─────────────────────────────────────┐
  │  1. OBSERVE — Examine data/results  │
  └──────────────┬──────────────────────┘
                 ▼
  ┌─────────────────────────────────────┐
  │  2. HYPOTHESIZE — Formulate a       │
  │     testable hypothesis             │
  └──────────────┬──────────────────────┘
                 ▼
  ┌─────────────────────────────────────┐
  │  3. TEST — Run experiment/analysis  │
  │     to validate or refute           │
  └──────────────┬──────────────────────┘
                 ▼
  ┌─────────────────────────────────────┐
  │  4. CONCLUDE                        │
  │     ✓ Validated → Record finding    │
  │     ✗ Refuted → Update hypothesis   │
  │       and return to step 2          │
  └──────────────┬──────────────────────┘
                 ▼
  ┌─────────────────────────────────────┐
  │  5. ITERATE — Repeat until all key  │
  │     hypotheses are resolved         │
  └─────────────────────────────────────┘
```

### Orchestrator Agent

**Role:** Reads this ROADMAP, determines current phase, delegates to sub-agents, enforces the
scientific method loop, and tracks progress.

**Responsibilities:**
- Parse ROADMAP.md to determine which phase/task is next
- Delegate tasks to the appropriate sub-agent
- Validate deliverables after each sub-agent completes
- **Review the hypothesis log** after each iteration: decide whether to iterate again or move on
- Update checklist status in ROADMAP.md
- Decide when to move to the next phase

### Sub-Agent 1: EDA Agent

**Scope:** Phase 1 — Problem Understanding & Data Exploration

**Scientific method applied to EDA:**

| Step | EDA Example |
|------|-------------|
| **Observe** | Load data, compute summary statistics, plot distributions |
| **Hypothesize** | "Class imbalance > 80/20 will degrade recall" |
| **Test** | Measure class distribution, run a quick baseline to check recall |
| **Conclude** | Validated → plan oversampling. Refuted → update hypothesis |
| **Iterate** | New hypothesis: "Text length correlates with label" → test → conclude |

**Capabilities:**
- Load and profile datasets (summary statistics, distributions)
- Detect data quality issues (missing values, duplicates, outliers)
- Identify problem type (classification vs regression vs clustering)
- Generate visualizations in notebooks
- **Maintain a hypothesis log** in the EDA notebook (hypothesis, test, result, conclusion)
- Write findings to `notebooks/01_exploratory_data_analysis.ipynb`

**Inputs:** Raw data in `data/raw/`
**Outputs:** Completed EDA notebook with hypothesis log, data quality report

### Sub-Agent 2: Training Agent

**Scope:** Phases 2–4 — Baseline, Experimentation, Validation

**Scientific method applied to training:**

| Step | Training Example |
|------|-----------------|
| **Observe** | Baseline achieves F1=0.60, confusion matrix shows false negatives |
| **Hypothesize** | "Adding class weights will improve recall by 10%+" |
| **Test** | Train with class weights, evaluate on validation set |
| **Conclude** | Validated → keep change. Refuted → revert, try different approach |
| **Iterate** | New hypothesis: "Larger model will improve precision" → test → conclude |

**Capabilities:**
- Generate and preprocess training data (`make generate-data`, `make preprocess`)
- Run baseline experiments (`make experiment config=configs/experiment/baseline.yaml`)
- Implement new model adapters (following `ModelPort` protocol)
- Create experiment configs and run experiments
- Compare MLflow runs and select best model
- **Log each hypothesis with its experiment run ID** in MLflow tags
- Write and run tests (`make test-unit`, `make test-integration`)

**Inputs:** Preprocessed data in `data/processed/`, experiment configs
**Outputs:** Trained model artifacts, MLflow experiment runs (tagged with hypotheses), passing tests

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
 3. EDA Agent: OBSERVE data → HYPOTHESIZE → TEST → CONCLUDE
    ├── Hypothesis validated → record finding, try next hypothesis
    └── Hypothesis refuted → update hypothesis, loop back to step 3
 4. EDA Agent reports: all key hypotheses resolved
 5. Orchestrator validates Phase 1 deliverables → marks complete
 6. Orchestrator delegates to Training Agent for Phase 2
 7. Training Agent runs baseline → records metrics
 8. Orchestrator checks if baseline meets target → proceeds to Phase 3
 9. Training Agent: OBSERVE metrics → HYPOTHESIZE improvement → TEST → CONCLUDE
    ├── Target met → proceed to Phase 4
    └── Target not met → update hypothesis, loop back to step 9
10. Orchestrator validates Phase 4 (testing) → delegates to Deployment Agent
11. Deployment Agent builds, deploys, verifies
12. Orchestrator marks all phases complete
```

### Agent Instructions Location

Each agent reads its instructions from:
- **Orchestrator:** `ROADMAP.md` (this file) + `CLAUDE.md`
- **EDA Agent:** `notebooks/01_exploratory_data_analysis.ipynb` checklist
- **Training Agent:** `CLAUDE.md` (architecture rules) + `configs/` (experiment configs)
- **Deployment Agent:** `docs/runbooks/model-deployment.md` + `Makefile` commands
