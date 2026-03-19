# Claude Central — Global Context

This is the root context file for Claude Code operating in this repository.
Read this file at the start of every session. Sub-directories may have their own
CLAUDE.md files that extend (never override) these global rules.

## Repository Purpose
Single source of truth for Claude Code context, skills, MCP servers, evals,
and multi-agent workflows. Treat this as a senior AI engineer's operating system.

## Core Engineering Principles (Non-Negotiable)
- **Correctness first**: Tests before or alongside implementation. Never skip.
- **Explicit over implicit**: Type annotations everywhere. No `Any` without comment.
- **Fail loudly**: Raise specific exceptions. Never swallow errors silently.
- **Idempotency**: All infrastructure and data pipeline operations must be idempotent.
- **Observability**: Every non-trivial operation logs structured JSON to stdout.
- **Security**: Secrets via env vars or AWS Secrets Manager only. Never hardcode.

## Python Standards
- Python 3.12+ minimum. Use `uv` for package management.
- Ruff for linting + formatting (replaces black/isort/flake8).
- Pyright for static type checking (strict mode).
- Pytest for all tests. Minimum 80% coverage on new code.
- Prefer `asyncio` for I/O-bound work. Use `anyio` for library code.
- Pydantic v2 for all data models and validation.
- Use `structlog` for structured logging.

## TypeScript Standards
- TypeScript strict mode always.
- ESLint + Prettier enforced.
- Zod for runtime validation.
- Vitest for unit tests.

## AWS Conventions
- All resources tagged: `Project`, `Environment`, `Owner`, `CostCentre`.
- IAM: least privilege always. No wildcards on resource ARNs in prod.
- CDK for all infrastructure. No console clicks in prod.
- Prefer managed services (Fargate, Lambda, SageMaker) over self-managed EC2.

## Git Conventions
- Branches: `feat/`, `fix/`, `chore/`, `eval/` prefixes.
- Commits: Conventional Commits format (`feat(mcp): add retrieval tool`).
- PRs require passing CI + at least one passing eval suite.

## MCP Server Standards
- Use `fastmcp` (Python) for all MCP server implementations.
- Every tool must have a clear docstring — this becomes the tool description.
- Every tool must have a corresponding benchmark and at least 5 eval cases.
- Servers run on stdio transport for local use, SSE for deployed use.

## Skill Usage
When asked to perform a task that matches a skill in `skills/`, read the
corresponding SKILL.md before starting. Skills encode hard-won patterns.

## When Unsure
Ask for clarification rather than assuming. State your assumptions explicitly
before implementing.
