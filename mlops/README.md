# MLOps

MLOps tooling and pipelines: feature engineering, experiment tracking, model registry, and SageMaker pipelines.

## Modules

| Module | Purpose |
|---|---|
| `feature_store.py` | Feature engineering pipeline |
| `experiment_tracking.py` | MLflow/W&B wrapper |
| `model_registry.py` | Model versioning abstraction |
| `sagemaker_pipeline.py` | AWS SageMaker Pipeline definition |

## Running Locally

```bash
# Start MLflow tracking server
mlflow server --host 0.0.0.0 --port 5000

# Run an experiment
cd mlops
uv run python -m mlops.experiment_tracking
```

## Infrastructure

SageMaker pipelines and S3 buckets are defined in `infra/lib/stacks/mlops-stack.ts`.
