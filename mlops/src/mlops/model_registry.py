"""
Model versioning abstraction.
Wraps MLflow Model Registry with a clean, typed interface.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import structlog

log = structlog.get_logger()


class ModelStage(str, Enum):
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"


@dataclass
class ModelVersion:
    name: str
    version: str
    stage: ModelStage
    run_id: str
    artifact_uri: str


class ModelRegistry:
    """
    Abstraction over MLflow Model Registry.
    Provides typed access to model versions and stage transitions.
    """

    def __init__(self, tracking_uri: str | None = None) -> None:
        import mlflow

        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        self._client = mlflow.tracking.MlflowClient()

    def register(self, run_id: str, artifact_path: str, model_name: str) -> ModelVersion:
        """Register a model from a run into the model registry."""
        import mlflow

        model_uri = f"runs:/{run_id}/{artifact_path}"
        result = mlflow.register_model(model_uri, model_name)
        log.info("model_registered", name=model_name, version=result.version, run_id=run_id)
        return ModelVersion(
            name=model_name,
            version=result.version,
            stage=ModelStage.STAGING,
            run_id=run_id,
            artifact_uri=model_uri,
        )

    def promote(self, name: str, version: str, stage: ModelStage) -> None:
        """Transition a model version to a new stage."""
        self._client.transition_model_version_stage(
            name=name, version=version, stage=stage.value
        )
        log.info("model_promoted", name=name, version=version, stage=stage.value)

    def get_production(self, name: str) -> ModelVersion | None:
        """Get the current production version of a model, or None if not found."""
        versions = self._client.get_latest_versions(name, stages=[ModelStage.PRODUCTION.value])
        if not versions:
            return None
        v = versions[0]
        return ModelVersion(
            name=name,
            version=v.version,
            stage=ModelStage.PRODUCTION,
            run_id=v.run_id,
            artifact_uri=v.source,
        )
