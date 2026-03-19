"""
Knowledge Base MCP Server.
Provides semantic search over a document corpus via ChromaDB + Anthropic embeddings.
Run locally: fastmcp dev src/knowledge_base/server.py
Deploy: Docker + ECS (see infra/lib/stacks/mcp-server-stack.ts)
"""
from __future__ import annotations

import os

import chromadb
import structlog
from anthropic import AsyncAnthropic
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from knowledge_base import __version__

log = structlog.get_logger().bind(service="knowledge-base", version=__version__)

mcp = FastMCP(
    name="knowledge-base",
    version=__version__,
    instructions=(
        "Semantic search over the internal knowledge base. "
        "Use search_documents when answering questions that require "
        "grounding in internal documentation. "
        "Use ingest_document to add new documents to the knowledge base."
    ),
)

_chroma = chromadb.Client()
_collection = _chroma.get_or_create_collection("docs")
_anthropic = AsyncAnthropic()


class SearchInput(BaseModel):
    query: str = Field(..., description="Natural language search query")
    top_k: int = Field(5, ge=1, le=20, description="Number of results to return")


class IngestInput(BaseModel):
    content: str = Field(..., description="Document text to ingest")
    source: str = Field(..., description="Source identifier (URL, filename, etc.)")
    metadata: dict = Field(default_factory=dict)


@mcp.tool()
async def search_documents(input: SearchInput) -> list[dict]:
    """
    Semantically search the knowledge base for documents relevant to the query.
    Returns a ranked list of {content, source, score} dicts (score 0.0-1.0, higher is better).
    Use this to answer questions grounded in internal documentation.
    """
    log.info("search_documents", query=input.query, top_k=input.top_k)
    results = _collection.query(
        query_texts=[input.query],
        n_results=input.top_k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "content": doc,
            "source": meta.get("source", "unknown"),
            "score": round(1 - dist, 4),
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


@mcp.tool()
async def ingest_document(input: IngestInput) -> dict:
    """
    Ingest a document into the knowledge base.
    The document will be available for semantic search immediately.
    Ingestion is idempotent — re-ingesting the same source+content is a no-op.
    Returns {id, status}.
    """
    import hashlib

    doc_id = hashlib.sha256(f"{input.source}:{input.content}".encode()).hexdigest()[:16]
    log.info("ingest_document", source=input.source, doc_id=doc_id)
    _collection.upsert(
        ids=[doc_id],
        documents=[input.content],
        metadatas=[{"source": input.source, **input.metadata}],
    )
    return {"id": doc_id, "status": "ingested"}


def main() -> None:
    transport = os.getenv("TRANSPORT", "stdio")
    port = int(os.getenv("PORT", "8080"))
    log.info("server_starting", transport=transport, port=port if transport == "sse" else None)
    if transport == "sse":
        mcp.run(transport="sse", port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
