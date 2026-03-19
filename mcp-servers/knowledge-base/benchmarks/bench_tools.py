"""
Latency benchmarks for knowledge-base MCP tools.
Usage: uv run python benchmarks/bench_tools.py
"""
from __future__ import annotations

import asyncio
import statistics
import time
from unittest.mock import MagicMock

from knowledge_base.tools import ingest, search


def _mock_collection(n_results: int = 5) -> MagicMock:
    col = MagicMock()
    col.query.return_value = {
        "documents": [["doc"] * n_results],
        "metadatas": [[{"source": f"s{i}"} for i in range(n_results)]],
        "distances": [[0.1 * i for i in range(n_results)]],
    }
    return col


async def bench_search(n: int = 200) -> None:
    col = _mock_collection()
    queries = [f"test query {i}" for i in range(n)]
    latencies: list[float] = []

    for q in queries:
        t0 = time.perf_counter()
        search(col, query=q, top_k=5)
        latencies.append((time.perf_counter() - t0) * 1000)

    latencies.sort()
    print(
        f"search ({n} calls) | "
        f"p50={statistics.median(latencies):.2f}ms | "
        f"p95={latencies[int(n * 0.95)]:.2f}ms | "
        f"p99={latencies[int(n * 0.99)]:.2f}ms"
    )


async def bench_ingest(n: int = 200) -> None:
    col = MagicMock()
    latencies: list[float] = []

    for i in range(n):
        t0 = time.perf_counter()
        ingest(col, content=f"document content {i}", source=f"doc{i}.md")
        latencies.append((time.perf_counter() - t0) * 1000)

    latencies.sort()
    print(
        f"ingest ({n} calls) | "
        f"p50={statistics.median(latencies):.2f}ms | "
        f"p95={latencies[int(n * 0.95)]:.2f}ms | "
        f"p99={latencies[int(n * 0.99)]:.2f}ms"
    )


async def main() -> None:
    print("=== Knowledge Base Benchmarks ===")
    await bench_search()
    await bench_ingest()


if __name__ == "__main__":
    asyncio.run(main())
