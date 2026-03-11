"""Post-generation hook for cookiecutter template.

Removes optional directories and files based on cookiecutter variables,
then initializes git and installs dependencies.
"""

import os
import shutil
import subprocess


def remove_path(path: str) -> None:
    """Remove a file or directory if it exists."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def main() -> None:
    # Remove optional directories based on cookiecutter choices
    if "{{ cookiecutter.include_notebooks }}" == "no":
        remove_path("notebooks")

    if "{{ cookiecutter.include_hyperparameter_tuning }}" == "no":
        remove_path("pipelines/hyperparameter_tuning")

    if "{{ cookiecutter.include_monitoring }}" != "full":
        remove_path("pipelines/monitoring")

    if "{{ cookiecutter.include_docs_site }}" == "no":
        remove_path("mkdocs.yml")
        remove_path("docs/mkdocs")

    if "{{ cookiecutter.include_auth }}" == "none":
        remove_path(
            os.path.join(
                "src",
                "{{ cookiecutter.project_slug }}",
                "adapters",
                "inbound",
                "middleware",
                "auth.py",
            )
        )

    if "{{ cookiecutter.data_versioning }}" == "none":
        remove_path(".dvc")
        remove_path(".dvcignore")

    if "{{ cookiecutter.ci_provider }}" == "gitlab_ci":
        remove_path(".github")
    elif "{{ cookiecutter.ci_provider }}" == "github_actions":
        remove_path(".gitlab-ci.yml")

    if "{{ cookiecutter.container_registry }}" == "none":
        remove_path(
            os.path.join(".github", "workflows", "deploy.yml")
            if os.path.exists(os.path.join(".github", "workflows", "deploy.yml"))
            else ""
        )

    # Remove batch inference files if not using batch serving
    if "{{ cookiecutter.serving_type }}" == "rest":
        remove_path("pipelines/batch_inference.py")

    # Initialize git repository
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial project from cookiecutter-ml-hexagonal"],
        check=True,
    )

    # Install dependencies with uv
    print("\n🔧 Installing dependencies with uv...")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("✅ Dependencies installed successfully")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   Then run: uv sync")

    # Install pre-commit hooks
    print("\n🔧 Setting up pre-commit hooks...")
    try:
        subprocess.run(["uv", "run", "pre-commit", "install"], check=True)
        print("✅ Pre-commit hooks installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Could not install pre-commit hooks. Run: uv run pre-commit install")

    print("\n🎉 Project '{{ cookiecutter.project_name }}' created successfully!")
    print("   cd {{ cookiecutter.project_slug }}")
    print("   make check  # Run lint + typecheck + tests")
    print("   make serve   # Start API server")


if __name__ == "__main__":
    main()
