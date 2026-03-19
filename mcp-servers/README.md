# MCP Servers

Custom MCP (Model Context Protocol) server implementations.

## Servers

| Server | Description | Status |
|---|---|---|
| `knowledge-base` | Semantic search over document corpus (ChromaDB) | In progress |
| `code-tools` | Repo analysis and code search tools | Stub |

## Running Locally

```bash
# knowledge-base
cd mcp-servers/knowledge-base
uv run fastmcp dev src/knowledge_base/server.py

# code-tools
cd mcp-servers/code-tools
uv run fastmcp dev src/code_tools/server.py
```

## Standards

All MCP servers in this repo must follow the `mcp-server` skill (`skills/mcp-server/SKILL.md`):
- FastMCP for all implementations
- Pydantic input models for every tool
- Docstrings written for the LLM (these become tool descriptions)
- Benchmark results recorded in each server's README
- At least 5 eval cases per tool

## Deployment

See `infra/lib/stacks/mcp-server-stack.ts` for Fargate deployment.
Deployed servers use SSE transport on port 8080.
