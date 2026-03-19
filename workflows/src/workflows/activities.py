"""
Shared activity definitions.
Activities are the only place where non-deterministic I/O is allowed.
Each activity is retryable — make them idempotent where possible.
"""
from __future__ import annotations

import structlog
from temporalio import activity

log = structlog.get_logger()


@activity.defn
async def call_llm(prompt: str, model: str = "claude-sonnet-4-6", max_tokens: int = 1024) -> str:
    """
    Generic LLM call activity. Retryable — Anthropic API is idempotent for reads.
    Returns the text content of the first message block.
    """
    import anthropic

    client = anthropic.AsyncAnthropic()
    log.info("llm_call_start", model=model, prompt_len=len(prompt))
    msg = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    result = msg.content[0].text  # type: ignore[union-attr]
    log.info("llm_call_complete", output_len=len(result))
    return result


@activity.defn
async def store_result(key: str, value: str) -> dict:
    """
    Persist a result to storage (stub — implement with S3/DynamoDB as needed).
    Idempotent: same key + value always produces same stored state.
    """
    log.info("store_result", key=key, value_len=len(value))
    # TODO: implement with boto3 S3/DynamoDB
    return {"key": key, "status": "stored"}
