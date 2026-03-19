"""
Async parallel eval runner.
Usage: python -m evals.framework.runner --suite prompt_quality
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Awaitable, Callable

import structlog

log = structlog.get_logger()


@dataclass
class EvalCase:
    id: str
    input: dict
    expected: dict
    metadata: dict = field(default_factory=dict)


@dataclass
class EvalResult:
    case_id: str
    score: float  # 0.0 - 1.0
    passed: bool
    latency_ms: float
    details: dict = field(default_factory=dict)


async def run_eval_suite(
    cases: list[EvalCase],
    runner_fn: Callable[[EvalCase], Awaitable[EvalResult]],
    concurrency: int = 10,
) -> list[EvalResult]:
    """Run eval cases in parallel with bounded concurrency."""
    sem = asyncio.Semaphore(concurrency)

    async def bounded(case: EvalCase) -> EvalResult:
        async with sem:
            t0 = time.perf_counter()
            result = await runner_fn(case)
            result.latency_ms = (time.perf_counter() - t0) * 1000
            return result

    results = await asyncio.gather(*[bounded(c) for c in cases])
    passed = sum(1 for r in results if r.passed)
    avg_latency = sum(r.latency_ms for r in results) / len(results) if results else 0.0

    log.info(
        "eval_suite_complete",
        total=len(results),
        passed=passed,
        pass_rate=f"{passed / len(results):.1%}" if results else "0%",
        avg_latency_ms=round(avg_latency, 1),
    )
    return list(results)
