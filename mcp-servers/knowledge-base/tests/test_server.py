"""Unit tests for knowledge-base MCP server tools."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from knowledge_base.tools import ingest, search


@pytest.fixture
def mock_collection() -> MagicMock:
    col = MagicMock()
    col.query.return_value = {
        "documents": [["Document about RAG", "Document about embeddings"]],
        "metadatas": [[{"source": "doc1.md"}, {"source": "doc2.md"}]],
        "distances": [[0.1, 0.3]],
    }
    return col


def test_search_returns_ranked_results(mock_collection: MagicMock) -> None:
    results = search(mock_collection, query="retrieval augmented generation", top_k=2)
    assert len(results) == 2
    assert results[0]["score"] > results[1]["score"]


def test_search_result_structure(mock_collection: MagicMock) -> None:
    results = search(mock_collection, query="test", top_k=1)
    assert set(results[0].keys()) == {"content", "source", "score"}


def test_search_score_clamped_to_valid_range(mock_collection: MagicMock) -> None:
    results = search(mock_collection, query="test", top_k=2)
    for result in results:
        assert 0.0 <= result["score"] <= 1.0


def test_ingest_returns_id_and_status() -> None:
    col = MagicMock()
    result = ingest(col, content="Hello world", source="test.md")
    assert result["status"] == "ingested"
    assert len(result["id"]) == 16


def test_ingest_is_idempotent() -> None:
    col = MagicMock()
    result1 = ingest(col, content="Same content", source="same.md")
    result2 = ingest(col, content="Same content", source="same.md")
    assert result1["id"] == result2["id"]
    assert col.upsert.call_count == 2  # called twice, but same id


def test_ingest_different_sources_different_ids() -> None:
    col = MagicMock()
    r1 = ingest(col, content="content", source="a.md")
    r2 = ingest(col, content="content", source="b.md")
    assert r1["id"] != r2["id"]
