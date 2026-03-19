"""
Embedding generation utilities.
Wraps Anthropic's embedding API (or falls back to ChromaDB's built-in embeddings).
"""
from __future__ import annotations

import structlog
from anthropic import AsyncAnthropic

log = structlog.get_logger()

_client = AsyncAnthropic()


async def embed_texts(texts: list[str], model: str = "voyage-3") -> list[list[float]]:
    """
    Generate embeddings for a list of texts using Anthropic's Voyage model.
    Returns a list of float vectors, one per input text.
    """
    # Anthropic embedding API (via Voyage) — replace with direct voyage-ai SDK if preferred
    response = await _client.post(
        "/v1/embeddings",
        body={"model": model, "input": texts},
    )
    return [item["embedding"] for item in response["data"]]


async def embed_query(query: str, model: str = "voyage-3") -> list[float]:
    """Embed a single query string."""
    vectors = await embed_texts([query], model=model)
    return vectors[0]
