"""
Experiment tracking wrapper.
Abstracts over MLflow and W&B with a unified interface.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Generator

import structlog

log = structlog.get_logger()


class ExperimentTracker:
    """
    Unified experiment tracking interface.
    Backed by MLflow locally, W&B in CI/prod.
    """

    def __init__(self, experiment_name: str, backend: str = "mlflow") -> None:
        self.experiment_name = experiment_name
        self.backend = backend
        self._run: Any = None

    def start_run(self, run_name: str | None = None, tags: dict | None = None) -> None:
        if self.backend == "mlflow":
            import mlflow

            mlflow.set_experiment(self.experiment_name)
            self._run = mlflow.start_run(run_name=run_name, tags=tags or {})
        elif self.backend == "wandb":
            import wandb

            self._run = wandb.init(
                project=self.experiment_name,
                name=run_name,
                tags=list((tags or {}).keys()),
            )
        log.info("experiment_run_started", experiment=self.experiment_name, run=run_name)

    def log_params(self, params: dict) -> None:
        if self.backend == "mlflow":
            import mlflow
            mlflow.log_params(params)
        elif self.backend == "wandb" and self._run:
            self._run.config.update(params)

    def log_metrics(self, metrics: dict, step: int | None = None) -> None:
        if self.backend == "mlflow":
            import mlflow
            mlflow.log_metrics(metrics, step=step)
        elif self.backend == "wandb" and self._run:
            self._run.log(metrics, step=step)

    def end_run(self) -> None:
        if self.backend == "mlflow":
            import mlflow
            mlflow.end_run()
        elif self.backend == "wandb" and self._run:
            self._run.finish()
        log.info("experiment_run_ended", experiment=self.experiment_name)

    @contextmanager
    def run(
        self, run_name: str | None = None, tags: dict | None = None
    ) -> Generator["ExperimentTracker", None, None]:
        self.start_run(run_name=run_name, tags=tags)
        try:
            yield self
        finally:
            self.end_run()
