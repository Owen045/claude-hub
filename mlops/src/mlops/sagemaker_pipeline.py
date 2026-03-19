"""
AWS SageMaker Pipeline definition.
Defines a training + evaluation pipeline as code.
"""
from __future__ import annotations

import os

import structlog

log = structlog.get_logger()


def build_pipeline(
    role_arn: str,
    bucket: str,
    pipeline_name: str = "claude-central-training",
    region: str | None = None,
) -> "sagemaker.workflow.pipeline.Pipeline":  # type: ignore[name-defined]
    """
    Build and return a SageMaker Pipeline.
    Does not start execution — call pipeline.upsert() then pipeline.start().
    """
    import boto3
    import sagemaker
    from sagemaker.inputs import TrainingInput
    from sagemaker.sklearn import SKLearn
    from sagemaker.workflow.parameters import ParameterFloat, ParameterString
    from sagemaker.workflow.pipeline import Pipeline
    from sagemaker.workflow.steps import TrainingStep

    region = region or os.getenv("AWS_REGION", "eu-west-2")
    session = sagemaker.Session(boto_session=boto3.Session(region_name=region))

    # Pipeline parameters
    model_approval_status = ParameterString(
        name="ModelApprovalStatus", default_value="PendingManualApproval"
    )
    accuracy_threshold = ParameterFloat(name="AccuracyThreshold", default_value=0.8)

    # Training step (stub — replace with real estimator)
    estimator = SKLearn(
        entry_point="train.py",
        role=role_arn,
        instance_type="ml.m5.large",
        framework_version="1.2-1",
        sagemaker_session=session,
        output_path=f"s3://{bucket}/models",
    )

    training_step = TrainingStep(
        name="TrainModel",
        estimator=estimator,
        inputs={
            "train": TrainingInput(
                s3_data=f"s3://{bucket}/data/train",
                content_type="text/csv",
            )
        },
    )

    pipeline = Pipeline(
        name=pipeline_name,
        parameters=[model_approval_status, accuracy_threshold],
        steps=[training_step],
        sagemaker_session=session,
    )

    log.info("pipeline_built", name=pipeline_name, region=region)
    return pipeline
