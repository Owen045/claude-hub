"""
Prompt quality eval suite.
Measures whether Claude's responses to key conceptual questions are accurate and complete.
Usage: uv run python -m evals.suites.prompt_quality.eval
"""
from __future__ import annotations

import asyncio
from pathlib import Path

import anthropic
import structlog

from evals.framework.datasets import load_jsonl
from evals.framework.reporter import to_stdout
from evals.framework.runner import EvalCase, EvalResult, run_eval_suite
from evals.framework.scorers import llm_judge

log = structlog.get_logger()
_client = anthropic.AsyncAnthropic()

DATASET = Path(__file__).parent / "dataset.jsonl"
PASS_THRESHOLD = 0.75


async def run_case(case: EvalCase) -> EvalResult:
    # Get Claude's response to the prompt
    msg = await _client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": case.input["prompt"]}],
    )
    response = msg.content[0].text  # type: ignore[union-attr]

    # Judge: does the response cover the expected topic and keywords?
    criteria = (
        f"The response should explain: {case.expected['topic']}. "
        f"Key concepts to cover: {', '.join(case.expected.get('keywords', []))}."
    )
    score = await llm_judge(response, case.expected, criteria)

    return EvalResult(
        case_id=case.id,
        score=score,
        passed=score >= PASS_THRESHOLD,
        latency_ms=0,
        details={"response_preview": response[:200]},
    )


async def main() -> None:
    cases = load_jsonl(DATASET)
    results = await run_eval_suite(cases, run_case, concurrency=5)
    to_stdout(results, suite_name="prompt_quality")


if __name__ == "__main__":
    asyncio.run(main())
