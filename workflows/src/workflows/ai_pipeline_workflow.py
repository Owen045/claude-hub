"""
Durable AI pipeline workflow using Temporal.io.
Demonstrates: LLM call retries, multi-step orchestration, human-in-the-loop pause.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.common import RetryPolicy


@dataclass
class PipelineInput:
    document: str
    task: str


@dataclass
class PipelineResult:
    summary: str
    critique: str
    final_output: str


# --- Activities (all I/O lives here) ---

@activity.defn
async def summarise_document(document: str) -> str:
    import anthropic

    client = anthropic.AsyncAnthropic()
    msg = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Summarise:\n\n{document}"}],
    )
    return msg.content[0].text  # type: ignore[union-attr]


@activity.defn
async def critique_summary(summary: str) -> str:
    import anthropic

    client = anthropic.AsyncAnthropic()
    msg = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Critique this summary:\n\n{summary}"}],
    )
    return msg.content[0].text  # type: ignore[union-attr]


# --- Workflow (deterministic orchestration only) ---

DEFAULT_RETRY = RetryPolicy(maximum_attempts=3, backoff_coefficient=2.0)
ACTIVITY_TIMEOUT = timedelta(seconds=60)


@workflow.defn
class AIPipelineWorkflow:
    @workflow.run
    async def run(self, input: PipelineInput) -> PipelineResult:
        summary = await workflow.execute_activity(
            summarise_document,
            input.document,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=DEFAULT_RETRY,
        )
        critique = await workflow.execute_activity(
            critique_summary,
            summary,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=DEFAULT_RETRY,
        )
        return PipelineResult(
            summary=summary,
            critique=critique,
            final_output=f"{summary}\n\n---\nCritique: {critique}",
        )
