"""Dataset loading utilities for eval suites."""
from __future__ import annotations

import json
from pathlib import Path

from evals.framework.runner import EvalCase


def load_jsonl(path: str | Path) -> list[EvalCase]:
    """
    Load eval cases from a JSONL file.
    Each line must be a JSON object with at minimum: id, input, expected.
    """
    cases = []
    for i, line in enumerate(Path(path).read_text().splitlines()):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON on line {i + 1} of {path}: {e}") from e

        if "id" not in obj or "input" not in obj or "expected" not in obj:
            raise ValueError(
                f"Line {i + 1} of {path} missing required fields: id, input, expected"
            )

        cases.append(
            EvalCase(
                id=obj["id"],
                input=obj["input"],
                expected=obj["expected"],
                metadata=obj.get("metadata", {}),
            )
        )
    return cases
