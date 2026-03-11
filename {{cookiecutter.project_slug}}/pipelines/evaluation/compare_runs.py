"""Compare MLflow experiment runs side by side."""


def compare_runs(experiment_name: str = "{{ cookiecutter.project_slug }}") -> None:
    """Load all runs from an MLflow experiment and display comparison."""
    try:
        import mlflow
    except ImportError:
        print("MLflow required. Install with: uv add mlflow")
        return

    mlflow.set_tracking_uri("http://localhost:5000")

    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"No experiment found with name: {experiment_name}")
        return

    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

    if runs.empty:
        print("No runs found.")
        return

    metric_cols = [c for c in runs.columns if c.startswith("metrics.")]
    param_cols = [c for c in runs.columns if c.startswith("params.")]
    display_cols = ["run_id", "start_time", "status"] + param_cols + metric_cols

    available_cols = [c for c in display_cols if c in runs.columns]
    comparison = runs[available_cols].sort_values("start_time", ascending=False)

    print(f"\n{'='*80}")
    print(f"Experiment: {experiment_name} ({len(runs)} runs)")
    print(f"{'='*80}")
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    compare_runs()
