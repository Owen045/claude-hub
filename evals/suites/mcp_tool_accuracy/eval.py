"""
MCP tool accuracy eval suite.
Measures correctness of knowledge-base MCP tool outputs.
Usage: uv run python -m evals.suites.mcp_tool_accuracy.eval
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import MagicMock

import structlog

from evals.framework.datasets import load_jsonl
from evals.framework.reporter import to_stdout
from evals.framework.runner import EvalCase, EvalResult, run_eval_suite

log = structlog.get_logger()

DATASET = Path(__file__).parent / "dataset.jsonl"
PASS_THRESHOLD = 0.8


def _mock_populated_collection() -> MagicMock:
    """Create a mock collection pre-populated with test documents."""
    col = MagicMock()
    col.query.return_value = {
        "documents": [["RAG combines retrieval with LLM generation."]],
        "metadatas": [[{"source": "rag-intro.md"}]],
        "distances": [[0.15]],
    }
    return col


async def run_case(case: EvalCase) -> EvalResult:
    from knowledge_base.tools import ingest, search

    tool = case.input["tool"]
    col = _mock_populated_collection()
    score = 0.0
    details: dict = {}

    try:
        if tool == "search_documents":
            results = search(col, query=case.input["query"], top_k=case.input.get("top_k", 5))
            expected_keys = set(case.expected.get("result_keys", []))
            if results:
                actual_keys = set(results[0].keys())
                key_match = expected_keys.issubset(actual_keys) if expected_keys else True
                score = 1.0 if key_match else 0.5
            else:
                score = 1.0 if case.expected.get("graceful", True) else 0.0
            details = {"result_count": len(results)}

        elif tool == "ingest_document":
            result = ingest(
                col,
                content=case.input["content"],
                source=case.input["source"],
                metadata=case.input.get("metadata"),
            )
            expected_status = case.expected.get("status", "ingested")
            id_ok = len(result["id"]) == case.expected.get("id_length", 16)
            status_ok = result["status"] == expected_status
            score = 1.0 if (status_ok and id_ok) else 0.0
            details = {"result": result}

    except Exception as e:
        log.error("eval_case_error", case_id=case.id, error=str(e))
        score = 0.0
        details = {"error": str(e)}

    return EvalResult(
        case_id=case.id,
        score=score,
        passed=score >= PASS_THRESHOLD,
        latency_ms=0,
        details=details,
    )


async def main() -> None:
    cases = load_jsonl(DATASET)
    results = await run_eval_suite(cases, run_case, concurrency=10)
    to_stdout(results, suite_name="mcp_tool_accuracy")


if __name__ == "__main__":
    asyncio.run(main())
