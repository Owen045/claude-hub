---
name: python-refactor
description: >
  Use when refactoring Python code: extracting functions/classes, improving
  module structure, reducing complexity, or modernising to Python 3.12+ patterns.
  Triggers on: refactor, extract, clean up, restructure, split module, simplify.
triggers:
  - refactor
  - extract function
  - extract class
  - split module
  - simplify
  - clean up
  - "*.py"
---

# Python Refactor Skill

## When to Use This Skill
When asked to improve the structure, readability, or maintainability of existing
Python code without changing its external behaviour.

## Pre-Flight Checklist
Before starting:
- [ ] Read the file(s) being refactored completely
- [ ] Confirm existing test coverage (run `pytest --co -q` to list tests)
- [ ] Understand the public API — what must not change

## Step-by-Step Process
1. **Characterise the code**: identify smells (long function, duplicate logic, god object, etc.)
2. **Write tests first** if coverage is insufficient (see write-tests skill)
3. **Refactor in small steps** — one transformation at a time, tests green after each
4. **Apply patterns** (see below)
5. **Run type checks** and lint after each significant change

## Patterns and Examples

### Extract to Protocol (not ABC)
```python
# Before
class DatabaseBackend(ABC):
    @abstractmethod
    def query(self, sql: str) -> list[dict]: ...

# After — use Protocol for structural subtyping
from typing import Protocol

class DatabaseBackend(Protocol):
    def query(self, sql: str) -> list[dict]: ...
```

### Replace isinstance chains with dispatch
```python
# Before
def handle(event: dict) -> str:
    if event["type"] == "search":
        return handle_search(event)
    elif event["type"] == "ingest":
        return handle_ingest(event)

# After — Pydantic discriminated union
from pydantic import BaseModel
from typing import Literal, Annotated, Union

class SearchEvent(BaseModel):
    type: Literal["search"]
    query: str

class IngestEvent(BaseModel):
    type: Literal["ingest"]
    content: str

Event = Annotated[Union[SearchEvent, IngestEvent], Field(discriminator="type")]
```

## Common Mistakes to Avoid
- Don't change behaviour while refactoring — separate commits for behaviour changes.
- Don't over-abstract: three similar functions is not a pattern, five is.
- Don't remove type information to make code shorter.

## Quality Gates
- [ ] All existing tests still pass
- [ ] No new `Any` types introduced
- [ ] Pyright reports no new errors
- [ ] Ruff lint passes
- [ ] Public API unchanged (check `__init__.py` exports)
