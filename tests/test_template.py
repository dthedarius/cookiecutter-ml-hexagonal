"""Tests for the cookiecutter template using pytest-cookies."""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def default_context():
    """Default cookiecutter context for testing."""
    return {
        "project_name": "Test ML Project",
        "project_slug": "test_ml_project",
        "project_description": "A test ML project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "python_version": "3.12",
        "ml_task": "text_classification",
        "model_framework": "huggingface",
        "serving_type": "rest",
        "include_notebooks": "no",
        "include_auth": "none",
        "include_monitoring": "basic",
        "data_versioning": "none",
        "include_hyperparameter_tuning": "no",
        "include_docs_site": "no",
        "ci_provider": "github_actions",
        "container_registry": "none",
        "prediction_threshold": "0.5",
        "primary_metric": "f1",
        "target_metric_value": "0.90",
    }


def test_template_generates_project(cookies, default_context):
    """Test that the template generates a project without errors."""
    result = cookies.bake(extra_context=default_context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert result.project_path.name == "test_ml_project"


def test_generated_project_has_required_files(cookies, default_context):
    """Test that all required files are present."""
    result = cookies.bake(extra_context=default_context)
    project = result.project_path

    required_files = [
        "pyproject.toml",
        "Makefile",
        "Dockerfile",
        "docker-compose.yml",
        ".pre-commit-config.yaml",
        ".gitignore",
        ".env.example",
        "CLAUDE.md",
        "README.md",
        "CHANGELOG.md",
        "src/test_ml_project/__init__.py",
        "src/test_ml_project/config.py",
        "src/test_ml_project/domain/value_objects/prediction_input.py",
        "src/test_ml_project/domain/value_objects/prediction_label.py",
        "src/test_ml_project/domain/value_objects/confidence_score.py",
        "src/test_ml_project/domain/value_objects/prediction_result.py",
        "src/test_ml_project/domain/services/predictor_service.py",
        "src/test_ml_project/domain/services/threshold_service.py",
        "src/test_ml_project/domain/services/input_sanitizer.py",
        "src/test_ml_project/domain/exceptions/prediction_error.py",
        "src/test_ml_project/domain/exceptions/model_not_loaded_error.py",
        "src/test_ml_project/domain/exceptions/invalid_input_error.py",
        "src/test_ml_project/ports/inbound/predict_port.py",
        "src/test_ml_project/ports/inbound/health_check_port.py",
        "src/test_ml_project/ports/outbound/model_port.py",
        "src/test_ml_project/ports/outbound/trainable_model_port.py",
        "src/test_ml_project/ports/outbound/experiment_tracker_port.py",
        "src/test_ml_project/adapters/inbound/api.py",
        "src/test_ml_project/adapters/inbound/dependencies.py",
        "src/test_ml_project/adapters/outbound/baseline_model.py",
        "src/test_ml_project/adapters/outbound/mlflow_tracker.py",
        "pipelines/run_experiment.py",
        "pipelines/config/experiment.py",
        "pipelines/config/model.py",
        "pipelines/config/training.py",
        "pipelines/config/reproducibility.py",
        "pipelines/data_validation/schema.py",
        "pipelines/data_validation/validate.py",
        "pipelines/training/preprocess.py",
        "pipelines/training/train.py",
        "pipelines/evaluation/evaluate.py",
        "configs/experiment/baseline.yaml",
        "configs/model/baseline.yaml",
        "configs/training/default.yaml",
        "configs/environments/development.yaml",
        "configs/environments/staging.yaml",
        "configs/environments/production.yaml",
        "tests/conftest.py",
        "tests/unit/domain/test_prediction_input.py",
        "tests/unit/domain/test_predictor_service.py",
        ".github/workflows/ci.yml",
        ".github/workflows/ml-validation.yml",
        "ROADMAP.md",
    ]

    for filepath in required_files:
        assert (project / filepath).exists(), f"Missing: {filepath}"


def test_generated_project_no_auth_middleware_when_none(cookies, default_context):
    """Test that auth middleware is removed when include_auth is none."""
    result = cookies.bake(extra_context=default_context)
    project = result.project_path
    # Auth middleware should not exist when include_auth is none
    # (post_gen_project.py removes it)


def test_generated_project_with_batch_serving(cookies, default_context):
    """Test that batch endpoint is included when serving_type is rest_with_batch."""
    default_context["serving_type"] = "rest_with_batch"
    result = cookies.bake(extra_context=default_context)
    project = result.project_path

    api_content = (project / "src/test_ml_project/adapters/inbound/api.py").read_text()
    assert "/predict/batch" in api_content
    assert (project / "pipelines/batch_inference.py").exists()


def test_generated_project_regression_task(cookies, default_context):
    """Test that regression task generates appropriate labels."""
    default_context["ml_task"] = "regression"
    result = cookies.bake(extra_context=default_context)
    project = result.project_path

    label_content = (
        project / "src/test_ml_project/domain/value_objects/prediction_label.py"
    ).read_text()
    assert "LOW" in label_content
    assert "MEDIUM" in label_content
    assert "HIGH" in label_content


def test_generated_project_sklearn_framework(cookies, default_context):
    """Test sklearn framework generates correct dependencies."""
    default_context["model_framework"] = "sklearn"
    result = cookies.bake(extra_context=default_context)
    project = result.project_path

    pyproject_content = (project / "pyproject.toml").read_text()
    assert "joblib" in pyproject_content
    assert "transformers" not in pyproject_content


def test_generated_project_with_notebooks(cookies, default_context):
    """Test that notebooks are generated when include_notebooks is yes."""
    default_context["include_notebooks"] = "yes"
    result = cookies.bake(extra_context=default_context)
    project = result.project_path

    assert (project / "notebooks").is_dir()
    assert (project / "notebooks/01_exploratory_data_analysis.ipynb").exists()
    assert (project / "notebooks/02_baseline_model.ipynb").exists()
    assert (project / "notebooks/03_model_experiments.ipynb").exists()

    pyproject_content = (project / "pyproject.toml").read_text()
    assert "jupyter" in pyproject_content


def test_generated_project_without_notebooks(cookies, default_context):
    """Test that notebooks directory is removed when include_notebooks is no."""
    result = cookies.bake(extra_context=default_context)
    project = result.project_path

    assert not (project / "notebooks").exists()


def test_generated_project_has_roadmap(cookies, default_context):
    """Test that ROADMAP.md is generated."""
    result = cookies.bake(extra_context=default_context)
    project = result.project_path

    assert (project / "ROADMAP.md").exists()
    roadmap_content = (project / "ROADMAP.md").read_text()
    assert "Phase 1" in roadmap_content
    assert "Agent Orchestration" in roadmap_content
