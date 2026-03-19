"""
Tool handler functions — pure business logic, decoupled from the MCP server.
This module is importable by tests and benchmarks without starting the server.
"""
from __future__ import annotations

import hashlib

import chromadb
import structlog

log = structlog.get_logger()


def search(
    collection: chromadb.Collection,
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Run a semantic search against a ChromaDB collection."""
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
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


def ingest(
    collection: chromadb.Collection,
    content: str,
    source: str,
    metadata: dict | None = None,
) -> dict:
    """Upsert a document into a ChromaDB collection. Idempotent."""
    doc_id = hashlib.sha256(f"{source}:{content}".encode()).hexdigest()[:16]
    collection.upsert(
        ids=[doc_id],
        documents=[content],
        metadatas=[{"source": source, **(metadata or {})}],
    )
    log.info("document_ingested", source=source, doc_id=doc_id)
    return {"id": doc_id, "status": "ingested"}
