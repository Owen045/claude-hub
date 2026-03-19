"""
Scorer implementations for eval cases.
- exact_match: string equality
- contains_match: substring check
- llm_judge: Claude rates quality 0.0-1.0
- semantic_similarity: cosine similarity via embeddings (stub)
"""
from __future__ import annotations

import json

import anthropic
import structlog

log = structlog.get_logger()

_client = anthropic.AsyncAnthropic()


def exact_match(result: str, expected: str) -> float:
    """Returns 1.0 if result exactly matches expected, 0.0 otherwise."""
    return 1.0 if result.strip() == expected.strip() else 0.0


def contains_match(result: str, expected: str) -> float:
    """Returns 1.0 if expected is a substring of result, 0.0 otherwise."""
    return 1.0 if expected.lower() in result.lower() else 0.0


async def llm_judge(
    result: str,
    expected: dict,
    criteria: str,
    model: str = "claude-haiku-4-5-20251001",
) -> float:
    """
    Use Claude as a judge to score result quality.
    Returns a float 0.0-1.0.
    """
    prompt = f"""You are an impartial evaluator. Rate the quality of the result below.

Criteria: {criteria}
Expected characteristics: {json.dumps(expected)}
Result to evaluate: {result}

Respond with only valid JSON: {{"score": <float 0.0-1.0>, "reason": "<one sentence>"}}
"""
    msg = await _client.messages.create(
        model=model,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    try:
        data = json.loads(msg.content[0].text)  # type: ignore[union-attr]
        score = float(data["score"])
        log.debug("llm_judge", score=score, reason=data.get("reason"))
        return max(0.0, min(1.0, score))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        log.warning("llm_judge_parse_error", error=str(e))
        return 0.0


def semantic_similarity(result: str, expected: str) -> float:
    """
    Cosine similarity between result and expected embeddings.
    Stub — implement with voyage-3 embeddings when needed.
    """
    raise NotImplementedError("semantic_similarity requires embedding setup")
