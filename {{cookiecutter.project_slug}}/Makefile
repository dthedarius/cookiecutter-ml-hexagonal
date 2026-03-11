.PHONY: install lint format typecheck test test-unit test-integration check serve

install:
	uv sync --frozen

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

typecheck:
	uv run mypy src/

test:
	uv run pytest tests/ -v

test-unit:
	uv run pytest tests/unit/ -v

test-integration:
	uv run pytest tests/integration/ -v -m integration

check: lint typecheck test-unit

serve:
	uv run uvicorn {{ cookiecutter.project_slug }}.adapters.inbound.api:app --reload --port 8000

mlflow-ui:
	uv run mlflow ui --port 5000

# --- ML Pipeline ---

generate-data:
	uv run python pipelines/data_generation/generate.py

validate-data:
	PYTHONPATH=. uv run python -m pipelines.data_validation.validate

preprocess:
	uv run python pipelines/training/preprocess.py

train:
	uv run python pipelines/training/train.py

evaluate:
	uv run python pipelines/evaluation/evaluate.py

experiment:
	PYTHONPATH=src:. uv run python -m pipelines.run_experiment --config $(config)

experiment-all:
	@for f in configs/experiment/*.yaml; do \
		PYTHONPATH=src:. uv run python -m pipelines.run_experiment --config $$f; \
	done

compare:
	PYTHONPATH=src:. uv run python -m pipelines.evaluation.compare_runs

pipeline: generate-data validate-data preprocess train evaluate
	@echo "Full ML pipeline complete."

# --- Docker ---

docker-build:
	docker build -t {{ cookiecutter.project_slug }}:latest .

docker-up:
	docker compose up -d

docker-down:
	docker compose down
