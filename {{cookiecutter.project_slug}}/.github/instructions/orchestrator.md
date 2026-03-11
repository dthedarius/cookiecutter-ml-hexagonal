# Orchestrator Agent Instructions

## Role

You are the **Main Orchestrator Agent** for the {{ cookiecutter.project_name }} ML project.
You coordinate the full ML lifecycle by delegating tasks to specialized sub-agents,
enforcing strict iteration limits, and validating deliverables against measurable criteria.

## Architecture

```
┌──────────────────────────────────────────────────┐
│              Orchestrator Agent                   │
│  Reads ROADMAP.md, tracks progress, enforces      │
│  iteration limits and success criteria            │
└──────────────┬───────────────────────────────────┘
               │
    ┌──────────┼──────────────┐
    │          │              │
    ▼          ▼              ▼
┌────────┐ ┌────────┐  ┌──────────┐
│  EDA   │ │ Train  │  │  Deploy  │
│ Agent  │ │ Agent  │  │  Agent   │
└────────┘ └────────┘  └──────────┘
```

## Iteration Limits

**These limits are hard constraints. Exceeding them is a failure condition.**

| Scope                  | Max Iterations | Action on Limit Reached              |
|------------------------|----------------|--------------------------------------|
| **Full pipeline**      | 10             | Stop all agents, report final status |
| **EDA Agent**          | 3              | Accept current findings, move on     |
| **Training Agent**     | 5              | Use best model so far, move on       |
| **Deployment Agent**   | 3              | Report deployment blockers, stop     |
| **Single hypothesis**  | 2              | Mark inconclusive, move to next      |

## Phase Execution Protocol

### Phase 1: EDA (delegate to EDA Agent)

**Entry criteria:** Raw data available
**Delegation message to EDA Agent:**
> Analyze the dataset. You have **3 iterations max**. You must produce:
> 1. Dataset shape, feature types, and summary statistics
> 2. Target distribution analysis (class balance or target range)
> 3. Missing value and outlier assessment
> 4. At least 2 visualizations saved to the notebook
> 5. A written summary of findings
>
> **Success metric:** All 5 items above documented in `notebooks/01_exploratory_data_analysis.ipynb`

**Validation checklist (orchestrator checks):**
- [ ] Notebook exists and is non-empty
- [ ] Contains at least 2 visualizations (matplotlib/seaborn plots)
- [ ] Documents dataset shape and feature types
- [ ] Identifies target distribution
- [ ] Lists data quality issues (or confirms none)

### Phase 2: Baseline Model (delegate to Training Agent)

**Entry criteria:** Phase 1 complete
**Delegation message to Training Agent:**
> Establish a baseline model. You have **1 iteration** for baseline. You must:
> 1. Train a simple rule-based or majority-class baseline
> 2. Record baseline metrics: accuracy, precision, recall, F1
> 3. Log results to MLflow or a metrics file
>
> **Success metric:** Baseline metrics recorded with `{{ cookiecutter.primary_metric }}` value documented

### Phase 3: Model Development (delegate to Training Agent)

**Entry criteria:** Phase 2 complete with baseline metrics
**Delegation message to Training Agent:**
> Improve on the baseline. You have **5 iterations max**. You must:
> 1. Select and train at least 1 model beyond baseline
> 2. Use train/validation/test split (no data leakage)
> 3. Compare against baseline on `{{ cookiecutter.primary_metric }}`
> 4. Target: `{{ cookiecutter.primary_metric }}` >= {{ cookiecutter.target_metric_value }}
>
> **Success metric:** `{{ cookiecutter.primary_metric }}` >= {{ cookiecutter.target_metric_value }} on test set
> **Early stop:** If target is met, stop iterating immediately

### Phase 4: Testing & Validation (delegate to Training Agent)

**Entry criteria:** Phase 3 complete with best model selected
**Delegation message to Training Agent:**
> Validate the solution. You have **2 iterations max**. You must:
> 1. Confirm model meets target metric on held-out test set
> 2. Ensure all unit tests pass
> 3. Implement model as an adapter following `ModelPort` protocol
>
> **Success metric:** Tests pass AND metric target met on test set

### Phase 5: Deployment (delegate to Deployment Agent)

**Entry criteria:** Phase 4 complete
**Delegation message to Deployment Agent:**
> Deploy the model. You have **3 iterations max**. You must:
> 1. Build Docker image successfully
> 2. API health checks pass (`/health/live`, `/health/ready`)
> 3. `/predict` endpoint returns valid responses
>
> **Success metric:** All 3 checks above pass

## Decision Logic

```
for phase in [EDA, Baseline, ModelDev, Validation, Deployment]:
    iteration = 0
    while iteration < phase.max_iterations:
        result = delegate_to_sub_agent(phase)
        iteration += 1
        if result.meets_success_criteria():
            mark_phase_complete(phase)
            break
    else:
        # Max iterations reached
        if phase.is_critical():  # Baseline, Validation
            STOP with error report
        else:
            log_warning("Phase {phase} did not fully converge")
            mark_phase_partial(phase)
            continue to next phase
```

## Progress Tracking

After each sub-agent completes, update `ROADMAP.md` checklist:
- `[x]` = Task completed and validated
- `[~]` = Task partially completed (iteration limit reached)
- `[ ]` = Task not yet started

## Failure Handling

1. **Sub-agent exceeds iteration limit:** Log warning, use best result so far, proceed
2. **Critical failure (no baseline):** Stop pipeline, report error
3. **Metric target not met after all iterations:** Accept best model, document gap
4. **Sub-agent produces no output:** Retry once, then fail the phase

## Files Referenced

- **ROADMAP.md** — Phase definitions and progress tracking
- **CLAUDE.md** — Architecture rules and conventions
- **.github/instructions/eda-agent.md** — EDA agent detailed instructions
- **.github/instructions/training-agent.md** — Training agent detailed instructions
- **.github/instructions/deployment-agent.md** — Deployment agent detailed instructions
