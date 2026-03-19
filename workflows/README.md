# Workflows

Temporal.io durable workflow definitions for AI pipelines.

## What Is Temporal?
Temporal provides durable execution — workflows survive process crashes, network
failures, and even server restarts. Ideal for multi-step AI pipelines where
each LLM call is expensive and must be retried reliably.

## Key Rule
**Workflows are deterministic. Activities handle all I/O.**
- No `datetime.now()`, `random`, or network calls in workflow code.
- All LLM calls, DB writes, and API calls go in `@activity.defn` functions.

## Running Locally

```bash
# Start Temporal dev server
brew install temporal
temporal server start-dev

# Start the worker
cd workflows
uv run python -m workflows.worker
```

## Workflows

| Workflow | Description |
|---|---|
| `AIPipelineWorkflow` | Summarise + critique a document (demo of retry/orchestration) |

## See Also
`skills/temporal-workflow/SKILL.md` for implementation patterns and quality gates.
