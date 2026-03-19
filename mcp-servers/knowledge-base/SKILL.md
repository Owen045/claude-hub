---
name: knowledge-base-mcp
description: >
  Context for working on the knowledge-base MCP server specifically.
  Read this when modifying tools, embeddings, or tests in mcp-servers/knowledge-base/.
---

# Knowledge Base MCP Server

## What It Does
Provides semantic search over an internal document corpus using ChromaDB for
vector storage and Anthropic embeddings for encoding.

## Tools Exposed

| Tool | Input | Output |
|---|---|---|
| `search_documents` | `SearchInput(query, top_k)` | `list[{content, source, score}]` |
| `ingest_document` | `IngestInput(content, source, metadata)` | `{id, status}` |

## Architecture
```
server.py          FastMCP entrypoint, tool registration
tools.py           Tool handler functions (pure business logic)
embeddings.py      Embedding generation (Anthropic API)
```

## Running
```bash
# Dev mode (stdio, with inspector)
uv run fastmcp dev src/knowledge_base/server.py

# Production (SSE)
TRANSPORT=sse PORT=8080 uv run python -m knowledge_base.server
```

## Benchmarks (target)
| Metric | Target |
|---|---|
| search p50 | < 50ms |
| search p95 | < 200ms |
| ingest p95 | < 500ms |
