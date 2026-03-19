"""Results output for eval suites: JSON, HTML, and Weights & Biases."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import structlog

from evals.framework.runner import EvalResult

log = structlog.get_logger()


def to_json(results: list[EvalResult], output_path: str | Path) -> None:
    """Write eval results to a JSON file."""
    data = {
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.passed),
            "pass_rate": sum(1 for r in results if r.passed) / len(results) if results else 0.0,
            "avg_latency_ms": sum(r.latency_ms for r in results) / len(results) if results else 0.0,
        },
        "results": [asdict(r) for r in results],
    }
    Path(output_path).write_text(json.dumps(data, indent=2))
    log.info("results_written", path=str(output_path))


def to_stdout(results: list[EvalResult], suite_name: str = "") -> None:
    """Print a summary table to stdout."""
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"\n{'=' * 50}")
    print(f"Eval Suite: {suite_name or 'unknown'}")
    print(f"Passed: {passed}/{total} ({passed/total:.0%})")
    print(f"Avg latency: {sum(r.latency_ms for r in results)/total:.0f}ms")
    print(f"{'=' * 50}")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"  [{status}] {r.case_id} (score={r.score:.2f}, {r.latency_ms:.0f}ms)")


def to_wandb(results: list[EvalResult], suite_name: str, run_name: str | None = None) -> None:
    """Log eval results to Weights & Biases."""
    try:
        import wandb
    except ImportError:
        log.warning("wandb_not_installed", msg="pip install wandb to enable W&B logging")
        return

    passed = sum(1 for r in results if r.passed)
    with wandb.init(project="claude-central-evals", name=run_name or suite_name) as run:
        run.log({
            f"{suite_name}/pass_rate": passed / len(results),
            f"{suite_name}/avg_latency_ms": sum(r.latency_ms for r in results) / len(results),
            f"{suite_name}/passed": passed,
            f"{suite_name}/total": len(results),
        })
        log.info("wandb_logged", suite=suite_name)
