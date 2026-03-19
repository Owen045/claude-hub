# Python Standards

## Tooling
- **Runtime**: Python 3.12+ minimum.
- **Package manager**: `uv` (workspace mode for monorepo). Never use pip directly.
- **Linting + formatting**: Ruff (replaces black, isort, flake8).
- **Type checking**: Pyright in strict mode. Run via `pyright` or `basedpyright`.
- **Testing**: Pytest with `pytest-asyncio` (asyncio_mode = "auto").

## Type Annotations
- All function signatures fully annotated — parameters and return types.
- No bare `Any`. If unavoidable, add `# type: ignore[assignment]  # reason`.
- Use `TypeAlias` for complex types. Use `TypeVar` for generic functions.
- Prefer `str | None` over `Optional[str]` (Python 3.10+ union syntax).

## Data Models
- All external data (API responses, tool inputs/outputs) validated with Pydantic v2.
- Use `model_config = ConfigDict(frozen=True)` for value objects.
- Use `Field(...)` with `description=` for MCP tool inputs (becomes LLM-visible docs).

## Async Patterns
- Prefer `async def` for any I/O-bound function (HTTP, DB, file).
- Use `asyncio.gather` for parallel async operations.
- Use `anyio` for library code that should be backend-agnostic.
- Never call `asyncio.run()` inside an already-running event loop.

## Logging
- Use `structlog` for all logging. Never use `print()` in library code.
- Bind context early: `log = structlog.get_logger().bind(service="my-service")`.
- Log at INFO for normal operations, WARNING for recoverable issues, ERROR for failures.
- Always include `duration_ms` for operations that call external services.

## Error Handling
- Define custom exception classes per domain: `class RetrievalError(Exception): ...`
- Include context in exception messages: `raise RetrievalError(f"Query failed: {query!r}")`
- Use `contextlib.suppress` only when silence is explicitly intentional.

## Project Layout
```
my-package/
├── pyproject.toml
└── src/
    └── my_package/
        ├── __init__.py      # Public API exports only
        ├── server.py        # Entrypoint
        └── ...
tests/
└── test_*.py
```
