# Claude Central

Single source of truth for Claude Code context, reusable skills, MCP servers, evals, and multi-agent workflows.

## Structure

| Directory | Purpose |
|---|---|
| `context/` | Shared Claude Code context fragments (engineering standards, conventions) |
| `skills/` | Reusable Claude Code skill definitions — read before starting matching tasks |
| `mcp-servers/` | Custom MCP server implementations (FastMCP, Python) |
| `agents/` | Multi-agent orchestration workflows (LangGraph) |
| `workflows/` | Temporal.io durable workflow definitions |
| `evals/` | Eval framework and test suites |
| `mlops/` | MLOps tooling and pipelines |
| `infra/` | AWS CDK infrastructure (TypeScript) |
| `scripts/` | Dev and CI helper scripts |

## Quick Start

```bash
# First-time setup
./scripts/bootstrap.sh

# Run all evals
./scripts/run_evals.sh

# Benchmark MCP servers
./scripts/bench_mcp.sh
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for Python package management
- Node.js 20+ and pnpm for CDK infra
- Copy `.env.example` to `.env` and fill in values

## Development Workflow

1. Read `CLAUDE.md` for global conventions.
2. Check `skills/` for a matching skill before starting any task.
3. All new code requires tests. All new MCP tools require evals.
4. Use Conventional Commits: `feat(scope): description`.

## Phase Roadmap

- **Phase 1** — Knowledge-base MCP server, Temporal AI pipeline, eval framework
- **Phase 2** — LangGraph multi-agent system, MLOps pipeline
- **Phase 3** — CDK deploy to Fargate, benchmarks, blog post
