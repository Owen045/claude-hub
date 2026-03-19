# Engineering Principles

## The Rule of Least Surprise
Write code that behaves exactly as its name and signature suggest.
A function called `get_user` should never modify state.

## Dependency Direction
High-level modules must not depend on low-level modules.
Both depend on abstractions (interfaces/protocols).
In Python: use `Protocol` classes for interfaces, not `ABC` inheritance.

## Error Handling Contract
Every function that can fail must either:
1. Return a `Result[T, E]` type (use `returns` library), OR
2. Raise a specific, documented exception type.
Never return `None` to signal failure — raise an exception.

## Testing Philosophy
- Unit tests: pure logic, no I/O, run in < 1ms each.
- Integration tests: real external calls, tagged `@pytest.mark.integration`.
- Eval tests: LLM quality measurement, tagged `@pytest.mark.eval`.
- All three categories run in CI; integration and eval can be skipped locally.

## Observability Requirements
Every service entrypoint must emit:
- Structured startup log with version, config (redacted secrets), environment.
- Request/operation duration as a histogram metric.
- Error rate as a counter metric.
Use OpenTelemetry SDK. Export to AWS X-Ray in prod, stdout locally.
