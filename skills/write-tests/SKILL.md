---
name: write-tests
description: >
  Use when writing pytest unit or integration tests for Python code.
  Triggers on: write tests, add tests, test coverage, pytest, unit test,
  integration test, test file, test suite.
triggers:
  - write tests
  - add tests
  - test coverage
  - pytest
  - unit test
  - integration test
  - "test_*.py"
---

# Write Tests Skill

## When to Use This Skill
Any time new tests are needed — whether covering existing code or written
alongside new implementation (TDD).

## Pre-Flight Checklist
- [ ] Read the code under test completely
- [ ] Identify: pure functions, I/O boundaries, error paths
- [ ] Decide test category: unit (no I/O) or integration (real I/O)

## Step-by-Step Process
1. **Map the surface**: list all public functions/methods and their behaviours
2. **Identify the I/O boundary**: what to mock vs what to call for real
3. **Write happy-path tests first**
4. **Write error/edge-case tests**
5. **Mark integration tests** with `@pytest.mark.integration`
6. **Check coverage**: `pytest --cov=src --cov-report=term-missing`

## Patterns and Examples

### Unit test (no I/O)
```python
import pytest
from my_package.utils import parse_score

def test_parse_score_valid() -> None:
    assert parse_score("0.85") == 0.85

def test_parse_score_out_of_range() -> None:
    with pytest.raises(ValueError, match="score must be between 0 and 1"):
        parse_score("1.5")
```

### Async unit test
```python
import pytest

@pytest.mark.asyncio
async def test_search_returns_ranked_results(mock_collection: MagicMock) -> None:
    result = await search_documents(SearchInput(query="test"))
    assert len(result) > 0
    assert result[0]["score"] >= result[-1]["score"]
```

### Integration test
```python
import pytest

@pytest.mark.integration
async def test_ingest_and_retrieve_roundtrip() -> None:
    await ingest_document(IngestInput(content="hello world", source="test"))
    results = await search_documents(SearchInput(query="hello"))
    assert any("hello" in r["content"] for r in results)
```

### Fixtures
```python
# conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_collection() -> MagicMock:
    col = MagicMock()
    col.query.return_value = {
        "documents": [["doc1", "doc2"]],
        "metadatas": [[{"source": "s1"}, {"source": "s2"}]],
        "distances": [[0.1, 0.3]],
    }
    return col
```

## Common Mistakes to Avoid
- Don't mock the thing you're testing — mock its dependencies.
- Don't use `time.sleep` in tests — use `freezegun` or mock time.
- Don't test implementation details — test observable behaviour.
- Don't write tests that pass trivially (asserting `True`).

## Quality Gates
- [ ] Unit tests run in < 1ms each (no I/O)
- [ ] Integration tests tagged `@pytest.mark.integration`
- [ ] Coverage ≥ 80% on new code
- [ ] No uncovered error paths
- [ ] `pytest -x` passes cleanly
