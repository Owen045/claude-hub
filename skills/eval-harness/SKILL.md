---
name: eval-harness
description: >
  Use when creating eval suites, LLM-as-judge scorers, or benchmark datasets.
  Triggers on: eval, evaluation, LLM judge, benchmark, dataset.jsonl, pass rate,
  eval suite, accuracy measurement, quality measurement.
triggers:
  - eval
  - evaluation
  - LLM judge
  - benchmark
  - "dataset.jsonl"
  - pass rate
  - quality measurement
---

# Eval Harness Skill

## When to Use This Skill
When adding eval cases for an MCP tool, agent, or prompt; or when building
a new eval suite from scratch.

## Pre-Flight Checklist
- [ ] Read `evals/framework/runner.py` to understand the EvalCase/EvalResult contract
- [ ] Identify what "correct" means for this task (exact match? semantic? LLM judge?)
- [ ] Prepare at least 5 diverse test cases (happy path, edge cases, failure modes)

## Step-by-Step Process
1. Write `dataset.jsonl` — one JSON object per line, with `id`, `input`, `expected`
2. Choose scorer: exact match, semantic similarity, or LLM-as-judge
3. Implement `eval.py` using `run_eval_suite` from the framework
4. Run and record baseline pass rate
5. Set pass rate threshold in CI (aim for > 80%)

## Dataset Format
```jsonl
{"id": "case-001", "input": {"query": "what is RAG?"}, "expected": {"topic": "retrieval augmented generation"}, "metadata": {"difficulty": "easy"}}
{"id": "case-002", "input": {"query": "explain attention mechanism"}, "expected": {"topic": "transformer attention"}, "metadata": {"difficulty": "medium"}}
```

## LLM-as-Judge Pattern
```python
import anthropic
import json

async def llm_judge(
    result: str,
    expected: dict,
    criteria: str,
) -> float:
    """Returns a score 0.0-1.0 from Claude acting as judge."""
    client = anthropic.AsyncAnthropic()
    prompt = f"""Rate the quality of this result on a scale of 0.0 to 1.0.

Criteria: {criteria}
Expected: {json.dumps(expected)}
Result: {result}

Respond with only a JSON object: {{"score": 0.0, "reason": "..."}}"""

    msg = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    data = json.loads(msg.content[0].text)
    return float(data["score"])
```

## Eval Suite Pattern
```python
# evals/suites/my_tool/eval.py
import asyncio
from evals.framework.runner import EvalCase, EvalResult, run_eval_suite
from evals.framework.datasets import load_jsonl

async def run_case(case: EvalCase) -> EvalResult:
    result = await my_tool(case.input)
    score = await llm_judge(str(result), case.expected, "relevance and correctness")
    return EvalResult(
        case_id=case.id,
        score=score,
        passed=score >= 0.8,
        latency_ms=0,  # filled by runner
        details={"result": result},
    )

async def main() -> None:
    cases = load_jsonl("evals/suites/my_tool/dataset.jsonl")
    results = await run_eval_suite(cases, run_case)

if __name__ == "__main__":
    asyncio.run(main())
```

## Common Mistakes to Avoid
- Don't use LLM-as-judge for cases with objectively correct answers — use exact match.
- Don't use GPT/other models as judge — use Claude for consistency.
- Don't write trivial cases that always pass — include genuine failure modes.
- Don't hardcode expected outputs for non-deterministic tasks — judge on criteria.

## Quality Gates
- [ ] At least 5 cases per tool/feature
- [ ] Cases cover: happy path, edge cases, at least one expected failure
- [ ] Baseline pass rate recorded in suite README
- [ ] Suite runs in < 60s total
- [ ] LLM judge prompts reviewed for bias
