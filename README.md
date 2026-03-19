# Claude Hub

A centralised repository for Claude Code configuration — context fragments, skills, MCP servers, evals, and multi-agent workflows. Clone it once, run the installer, and every Claude Code session picks up your standards and tools automatically.

## How it works

Claude Code loads `~/.claude/CLAUDE.md` at the start of every session, regardless of which project you're working in. `install.sh` generates that file with absolute-path imports pointing back into this repo, so your context and skill index are always loaded globally. MCP server registrations are merged into `~/.claude/settings.json` the same way.

```
claude-hub/
├── context/          # Engineering standards — imported into every session
├── skills/           # Task-specific prompt libraries — read on demand
├── mcp-servers/      # Custom MCP server implementations (FastMCP)
├── install/          # Install-time config fragments
│   └── settings-fragment.json   # MCP server definitions
├── install.sh        # Wires the repo into ~/.claude
├── agents/           # LangGraph multi-agent orchestration
├── workflows/        # Temporal.io durable workflow definitions
├── evals/            # Eval framework and test suites
├── mlops/            # MLOps tooling and SageMaker pipelines
├── infra/            # AWS CDK infrastructure (TypeScript)
└── scripts/          # Dev and CI helpers
```

## Installation

### Prerequisites

- Python 3.12+ and [uv](https://docs.astral.sh/uv/)
- Node.js 20+ and [pnpm](https://pnpm.io/) (for CDK infra only)
- [Claude Code](https://claude.ai/claude-code) CLI

### Install

```bash
git clone https://github.com/Owen045/claude-hub.git ~/Repos/claude-hub
cd ~/Repos/claude-hub

# Fill in API keys before running
cp .env.example .env
$EDITOR .env

# Wire everything into ~/.claude
./install.sh
```

Then **restart Claude Code**. From that point on, every session will have your context and skill index loaded.

### What the installer does

| Action | Detail |
|--------|--------|
| Generates `~/.claude/CLAUDE.md` | Imports all `context/` fragments and a skills index with absolute paths |
| Updates `~/.claude/settings.json` | Registers MCP servers (`knowledge-base`, `code-tools`) |
| Installs Python deps | `uv sync --all-packages` across the workspace |
| Installs Node deps | `pnpm install` for CDK infra |
| Scaffolds `.env` | Copies `.env.example` if no `.env` exists |

### Keeping up to date

```bash
git pull
./install.sh   # regenerates ~/.claude/CLAUDE.md with latest context and skills
```

The installer is idempotent — safe to re-run at any time.

## Context fragments

Files in `context/` are the single source of truth for engineering standards. They are imported into `~/.claude/CLAUDE.md` (global) and into the project-level `CLAUDE.md` via `@` imports. Edit them here and re-run `install.sh` to propagate changes everywhere.

| File | Covers |
|------|--------|
| `context/engineering-principles.md` | Correctness, error handling, observability, testing philosophy |
| `context/python-standards.md` | Tooling (uv, Ruff, Pyright), types, async, logging, project layout |
| `context/typescript-standards.md` | Strict mode, Zod, ESLint/Prettier, CDK patterns |
| `context/aws-conventions.md` | Tagging, IAM least-privilege, naming, service preferences |
| `context/git-conventions.md` | Branch naming, Conventional Commits, PR standards |

## Skills

Skills are task-specific prompt libraries stored as `SKILL.md` files. They contain pre-flight checklists, step-by-step processes, code patterns, and quality gates. Claude reads the relevant skill file before starting a matching task.

The global `~/.claude/CLAUDE.md` contains a skills index — a table of triggers that tells Claude which skill file to read. The full skill content is only loaded when needed, keeping baseline context lean.

| Skill | Triggers |
|-------|----------|
| `skills/python-refactor/` | refactor, extract, clean up, restructure Python |
| `skills/write-tests/` | write tests, add tests, pytest, coverage, unit test |
| `skills/aws-cdk-construct/` | CDK, AWS infra, CloudFormation, stack, Fargate, Lambda |
| `skills/temporal-workflow/` | Temporal, durable workflow, activity, worker |
| `skills/mcp-server/` | MCP server, FastMCP, tool definition, benchmark MCP |
| `skills/langgraph-agent/` | LangGraph, StateGraph, multi-agent, agent node |
| `skills/eval-harness/` | eval, LLM judge, benchmark, dataset.jsonl, pass rate |

### Adding a new skill

1. Copy `skills/_template/SKILL.md` to `skills/<your-skill>/SKILL.md`
2. Fill in the frontmatter (`name`, `description`, `triggers`) and the skill body
3. Add a row to the skills table in `CLAUDE.md` and `install/` template
4. Re-run `./install.sh` to update `~/.claude/CLAUDE.md`

## MCP servers

Custom servers live in `mcp-servers/`. They are registered in `~/.claude/settings.json` by `install.sh` using definitions from `install/settings-fragment.json`.

| Server | Description |
|--------|-------------|
| `mcp-servers/knowledge-base/` | Vector search over internal documents (ChromaDB + FastMCP) |
| `mcp-servers/code-tools/` | Code analysis and manipulation tools (FastMCP) |

To add a new server, implement it under `mcp-servers/<name>/` following the `mcp-server` skill, then add its registration to `install/settings-fragment.json` and re-run `install.sh`.

## Development

```bash
# Run all evals
./scripts/run_evals.sh

# Benchmark MCP servers
./scripts/bench_mcp.sh
```

All new MCP tools require:
- Pydantic input models
- A docstring written for the LLM
- At least 5 eval cases with > 80% pass rate
- A benchmark showing p95 < 200ms

## Phase Roadmap

- **Phase 1** — Knowledge-base MCP server, Temporal AI pipeline, eval framework
- **Phase 2** — LangGraph multi-agent system, MLOps pipeline
- **Phase 3** — CDK deploy to Fargate, benchmarks, blog post
