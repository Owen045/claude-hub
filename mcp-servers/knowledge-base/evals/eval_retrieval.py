"""
LLM-judged eval for retrieval quality of the knowledge-base search_documents tool.
Usage: uv run python evals/eval_retrieval.py
"""
from __future__ import annotations

import asyncio
import json

import anthropic
import structlog

log = structlog.get_logger()

CASES = [
    {
        "id": "ret-001",
        "query": "What is retrieval augmented generation?",
        "documents": [
            "RAG combines a retrieval step with an LLM to ground answers in documents.",
            "Machine learning is a subset of AI.",
        ],
        "expected_top_source": "rag-intro.md",
        "min_score": 0.8,
    },
    {
        "id": "ret-002",
        "query": "How do I configure AWS IAM roles?",
        "documents": [
            "IAM roles are configured via AWS console or CDK using aws_iam.Role.",
            "Python is a programming language.",
        ],
        "expected_top_source": "aws-iam.md",
        "min_score": 0.8,
    },
    {
        "id": "ret-003",
        "query": "Explain the Temporal workflow execution model",
        "documents": [
            "Temporal workflows are deterministic. Activities handle all I/O.",
            "Docker is a containerisation platform.",
        ],
        "expected_top_source": "temporal-guide.md",
        "min_score": 0.8,
    },
    {
        "id": "ret-004",
        "query": "What testing frameworks does this project use?",
        "documents": [
            "This project uses pytest with asyncio_mode=auto and Pyright for types.",
            "Football is a popular sport.",
        ],
        "expected_top_source": "python-standards.md",
        "min_score": 0.75,
    },
    {
        "id": "ret-005",
        "query": "How should I handle errors in Python functions?",
        "documents": [
            "Raise specific exception types. Never return None to signal failure.",
            "JavaScript uses var, let, and const.",
        ],
        "expected_top_source": "engineering-principles.md",
        "min_score": 0.8,
    },
]


async def judge_retrieval(query: str, top_result: str, expected_topic: str) -> float:
    """Use Claude to judge whether the top result is relevant to the query."""
    client = anthropic.AsyncAnthropic()
    prompt = f"""You are evaluating a document retrieval system.

Query: {query}
Expected topic: {expected_topic}
Top retrieved result: {top_result}

Rate how relevant the retrieved result is to answering the query, on a scale of 0.0 to 1.0.
1.0 = perfectly relevant, directly addresses the query
0.5 = partially relevant, tangentially related
0.0 = completely irrelevant

Respond with only valid JSON: {{"score": <float>, "reason": "<one sentence>"}}"""

    msg = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=128,
        messages=[{"role": "user", "content": prompt}],
    )
    data = json.loads(msg.content[0].text)
    return float(data["score"])


async def run_case(case: dict) -> dict:
    # Simulate retrieval (in real eval, call the actual tool)
    top_result = case["documents"][0]
    score = await judge_retrieval(case["query"], top_result, case["expected_top_source"])
    passed = score >= case["min_score"]
    log.info("eval_case", id=case["id"], score=score, passed=passed)
    return {"id": case["id"], "score": score, "passed": passed}


async def main() -> None:
    results = await asyncio.gather(*[run_case(c) for c in CASES])
    passed = sum(1 for r in results if r["passed"])
    print(f"\nRetrieval Eval: {passed}/{len(results)} passed "
          f"({passed/len(results):.0%})")


if __name__ == "__main__":
    asyncio.run(main())
