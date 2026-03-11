from {{ cookiecutter.project_slug }}.adapters.outbound.baseline_model import BaselineModel
from {{ cookiecutter.project_slug }}.ports.outbound.trainable_model_port import TrainableModelPort


def test_baseline_model_satisfies_trainable_protocol() -> None:
    model: TrainableModelPort = BaselineModel()
    assert model is not None
