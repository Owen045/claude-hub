"""
Feature engineering pipeline.
Transforms raw data into ML-ready features with lineage tracking.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

import structlog

log = structlog.get_logger()


@dataclass
class FeatureSet:
    """A named, versioned collection of features."""

    name: str
    version: str
    features: dict[str, list]
    metadata: dict = field(default_factory=dict)


class FeatureTransform(Protocol):
    """Protocol for feature transformation steps."""

    def transform(self, data: dict) -> dict:
        """Apply transformation to raw data. Must be idempotent."""
        ...


@dataclass
class TextLengthFeature:
    """Extract text length as a feature."""

    field_name: str
    output_name: str | None = None

    def transform(self, data: dict) -> dict:
        output = self.output_name or f"{self.field_name}_length"
        return {output: len(str(data.get(self.field_name, "")))}


@dataclass
class FeaturePipeline:
    """Compose multiple feature transforms into a pipeline."""

    name: str
    transforms: list[FeatureTransform] = field(default_factory=list)

    def run(self, records: list[dict]) -> FeatureSet:
        """Apply all transforms to each record and return a FeatureSet."""
        log.info("feature_pipeline_start", name=self.name, n_records=len(records))
        all_features: dict[str, list] = {}

        for record in records:
            combined: dict = {}
            for transform in self.transforms:
                combined.update(transform.transform(record))
            for key, value in combined.items():
                all_features.setdefault(key, []).append(value)

        log.info("feature_pipeline_complete", name=self.name, n_features=len(all_features))
        return FeatureSet(name=self.name, version="latest", features=all_features)
