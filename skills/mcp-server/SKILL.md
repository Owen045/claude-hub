---
name: mcp-server
description: >
  Use when building, extending, or benchmarking an MCP (Model Context Protocol)
  server. Triggers on: MCP server, FastMCP, tool definition, MCP tool, server.py
  in mcp-servers directory, benchmark MCP, eval MCP tools.
---

# MCP Server Skill

## Framework: FastMCP (Python)

Always use `fastmcp` — it handles the protocol boilerplate.

## Minimal Server Template

```python
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="my-server",
    version="0.1.0",
    instructions="Describe what this server does for the LLM host.",
)

class SearchInput(BaseModel):
    query: str
    top_k: int = 5

@mcp.tool()
async def search_knowledge_base(input: SearchInput) -> list[dict]:
    """
    Search the internal knowledge base for relevant documents.
    Returns a list of {content, source, score} dicts ranked by relevance.
    Use this when you need to answer questions grounded in internal docs.
    """
    # Implementation here
    ...

if __name__ == "__main__":
    mcp.run()  # stdio transport (local)
    # mcp.run(transport="sse", port=8080)  # SSE transport (deployed)
```

## Tool Design Rules
1. Tool names must be verbs: `search_`, `create_`, `get_`, `list_`, `update_`.
2. Docstrings are the tool description seen by the LLM — write them for the model.
3. Input validation via Pydantic always. Never accept raw dicts.
4. Return structured data (list/dict), never raw strings unless unavoidable.
5. Every tool must be idempotent where possible.

## Benchmarking Template

```python
# benchmarks/bench_tools.py
import asyncio, time, statistics
from src.my_server.tools import search_knowledge_base

async def bench_search(n: int = 100):
    queries = ["test query"] * n
    latencies = []
    for q in queries:
        t0 = time.perf_counter()
        await search_knowledge_base(SearchInput(query=q))
        latencies.append((time.perf_counter() - t0) * 1000)
    print(f"p50={statistics.median(latencies):.1f}ms  "
          f"p95={statistics.quantiles(latencies, n=20)[18]:.1f}ms  "
          f"p99={sorted(latencies)[int(n*0.99)]:.1f}ms")
```

## Eval Template (LLM-as-Judge)

```python
# evals/eval_retrieval.py
CASES = [
    {"query": "...", "expected_topic": "...", "min_score": 0.8},
]

async def judge(result: list[dict], expected_topic: str) -> float:
    # Use Claude to score relevance 0.0-1.0
    ...
```

## Quality Gates
- [ ] All tools have Pydantic input models
- [ ] All tools have docstrings written for the LLM
- [ ] Benchmarks show p95 < 200ms for local tools
- [ ] At least 5 eval cases per tool with pass rate > 80%
- [ ] Server tested via `mcp dev src/server.py`
