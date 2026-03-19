# Claude Code — Centralised Context, Skills & Plugins Repo Bootstrap

> Give this file to Claude Code and say: **"Read this file carefully and scaffold the entire repo structure described within it, creating all files, directories, and starter code as specified."**

---

## Mission

Scaffold a monorepo called `claude-central` that acts as the single source of truth for all Claude Code context, reusable skills, MCP servers, evals, and multi-agent workflows. This repo is designed around a senior AI software engineer's portfolio — demonstrating core engineering principles alongside modern AI tooling.

---

## Repo Structure to Create

```
claude-central/
├── CLAUDE.md                          # Root Claude Code context file (global)
├── README.md                          # Human-readable overview
├── .cursorrules                        # Mirror of key CLAUDE.md rules for Cursor users
├── pyproject.toml                      # Root Python config (uv workspace)
├── package.json                        # Root Node config (pnpm workspace)
├── .env.example                        # Environment variable template
│
├── context/                            # Shared Claude Code context fragments
│   ├── engineering-principles.md       # Core engineering standards Claude must follow
│   ├── python-standards.md             # Python conventions, tooling, patterns
│   ├── typescript-standards.md         # TypeScript conventions
│   ├── aws-conventions.md              # AWS naming, IAM least-privilege, tagging
│   └── git-conventions.md             # Branch naming, commit format, PR standards
│
├── skills/                             # Reusable Claude Code skill definitions
│   ├── README.md
│   ├── _template/
│   │   └── SKILL.md                   # Template for creating new skills
│   ├── python-refactor/
│   │   └── SKILL.md
│   ├── write-tests/
│   │   └── SKILL.md
│   ├── aws-cdk-construct/
│   │   └── SKILL.md
│   ├── temporal-workflow/
│   │   └── SKILL.md
│   ├── mcp-server/
│   │   └── SKILL.md
│   ├── langgraph-agent/
│   │   └── SKILL.md
│   └── eval-harness/
│       └── SKILL.md
│
├── mcp-servers/                        # Custom MCP server implementations
│   ├── README.md
│   ├── knowledge-base/                 # MCP server: vector search over docs
│   │   ├── SKILL.md
│   │   ├── pyproject.toml
│   │   ├── src/
│   │   │   └── knowledge_base/
│   │   │       ├── __init__.py
│   │   │       ├── server.py           # FastMCP server entrypoint
│   │   │       ├── tools.py            # Tool definitions
│   │   │       └── embeddings.py       # Embedding logic
│   │   ├── tests/
│   │   │   └── test_server.py
│   │   ├── benchmarks/
│   │   │   └── bench_tools.py         # Latency/accuracy benchmarks
│   │   └── evals/
│   │       └── eval_retrieval.py       # LLM-judged eval for retrieval quality
│   └── code-tools/                     # MCP server: repo analysis tools
│       ├── SKILL.md
│       ├── pyproject.toml
│       └── src/
│           └── code_tools/
│               ├── __init__.py
│               └── server.py
│
├── agents/                             # Multi-agent orchestration workflows
│   ├── README.md
│   ├── orchestrator/                   # Central orchestrator agent
│   │   ├── CLAUDE.md                  # Sub-agent context (Claude Code reads this in subdir)
│   │   ├── pyproject.toml
│   │   └── src/
│   │       └── orchestrator/
│   │           ├── __init__.py
│   │           ├── graph.py            # LangGraph orchestration graph
│   │           ├── nodes.py            # Agent node definitions
│   │           ├── state.py            # Shared state schema (TypedDict/Pydantic)
│   │           └── prompts.py          # System prompts per agent role
│   ├── researcher/                     # Specialist: web research agent
│   │   └── src/researcher/
│   ├── coder/                          # Specialist: code generation agent
│   │   └── src/coder/
│   └── critic/                         # Specialist: review/eval agent
│       └── src/critic/
│
├── workflows/                          # Temporal.io durable workflow definitions
│   ├── README.md
│   ├── pyproject.toml
│   └── src/
│       └── workflows/
│           ├── __init__.py
│           ├── ai_pipeline_workflow.py  # Example: durable AI pipeline
│           ├── activities.py            # Activity definitions (LLM calls, I/O)
│           └── worker.py               # Temporal worker entrypoint
│
├── evals/                              # Eval framework and test suites
│   ├── README.md
│   ├── pyproject.toml
│   ├── framework/
│   │   ├── __init__.py
│   │   ├── runner.py                   # Eval runner (async, parallel)
│   │   ├── scorers.py                  # LLM-as-judge, exact match, semantic sim
│   │   ├── datasets.py                 # Dataset loading utilities
│   │   └── reporter.py                 # Results output (JSON, HTML, W&B)
│   └── suites/
│       ├── prompt_quality/
│       │   ├── dataset.jsonl
│       │   └── eval.py
│       ├── mcp_tool_accuracy/
│       │   ├── dataset.jsonl
│       │   └── eval.py
│       └── agent_task_completion/
│           ├── dataset.jsonl
│           └── eval.py
│
├── mlops/                              # MLOps tooling and pipelines
│   ├── README.md
│   ├── pyproject.toml
│   └── src/
│       └── mlops/
│           ├── __init__.py
│           ├── feature_store.py        # Feature engineering pipeline
│           ├── experiment_tracking.py  # MLflow/W&B wrapper
│           ├── model_registry.py       # Model versioning abstraction
│           └── sagemaker_pipeline.py   # AWS SageMaker Pipeline definition
│
├── infra/                              # AWS CDK infrastructure
│   ├── README.md
│   ├── package.json
│   ├── tsconfig.json
│   ├── cdk.json
│   └── lib/
│       ├── stacks/
│       │   ├── ai-pipeline-stack.ts    # Core AI pipeline stack
│       │   ├── mcp-server-stack.ts     # Containerised MCP server on ECS
│       │   └── mlops-stack.ts          # SageMaker + S3 + ECR
│       └── constructs/
│           ├── lambda-python.ts        # Opinionated Python Lambda construct
│           └── ecs-fastapi.ts          # FastAPI on Fargate construct
│
└── scripts/
    ├── bootstrap.sh                    # First-time dev setup
    ├── run_evals.sh                    # Run all eval suites
    └── bench_mcp.sh                    # Benchmark all MCP servers
```

---

## File Contents to Generate

### `/CLAUDE.md`

```markdown
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
```

---

### `/context/engineering-principles.md`

```markdown
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
```

---

### `/skills/_template/SKILL.md`

```markdown
---
name: [skill-name]
description: >
  One to three sentences describing when Claude Code should trigger this skill.
  Be specific about file types, task keywords, and scope. This description is
  used for automatic skill matching — precision matters.
triggers:
  - keyword patterns that should activate this skill
  - file types or extensions
  - task categories
---

# [Skill Name]

## When to Use This Skill
[Precise conditions. What problem does this solve?]

## Pre-Flight Checklist
Before starting:
- [ ] Check item 1
- [ ] Check item 2

## Step-by-Step Process
1. First do this
2. Then do that

## Patterns and Examples
[Concrete code examples with rationale]

## Common Mistakes to Avoid
[Anti-patterns with explanations]

## Quality Gates
Before considering this task done:
- [ ] Tests pass
- [ ] Types check
- [ ] Lint passes
- [ ] [Skill-specific quality check]
```

---

### `/skills/temporal-workflow/SKILL.md`

```markdown
---
name: temporal-workflow
description: >
  Use when creating, modifying, or debugging Temporal.io workflows and activities.
  Triggers on: Temporal, durable workflow, workflow definition, activity, worker,
  long-running process, retry logic, saga pattern.
---

# Temporal.io Workflow Skill

## Key Concepts to Apply
- **Workflows are deterministic**: No random, no datetime.now(), no direct I/O.
  All non-deterministic operations live in Activities.
- **Activities are the side-effects**: API calls, DB writes, LLM calls go here.
- **Workflows are resumable**: They can sleep for days. Design accordingly.

## Python Boilerplate

### Workflow Definition
```python
import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

@workflow.defn
class AIPipelineWorkflow:
    @workflow.run
    async def run(self, input: PipelineInput) -> PipelineResult:
        # Activities called via workflow.execute_activity
        result = await workflow.execute_activity(
            call_llm_activity,
            input.prompt,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        return PipelineResult(output=result)
```

### Activity Definition
```python
from temporalio import activity

@activity.defn
async def call_llm_activity(prompt: str) -> str:
    # All real I/O here — this is retryable
    client = anthropic.AsyncAnthropic()
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
```

## Quality Gates
- [ ] Workflow contains zero I/O calls
- [ ] All activities have explicit timeout + retry policy
- [ ] Worker registers both workflow and activity types
- [ ] Integration test covers happy path and at least one retry scenario
```

---

### `/skills/mcp-server/SKILL.md`

```markdown
---
name: mcp-server
description: >
  Use when building, extending, or benchmarking an MCP (Model Context Protocol)
  server. Triggers on: MCP server, FastMCP, tool definition, MCP tool, server.py
  in mcp-servers directory, benchmark MCP, eval MCP tools.
---

# MCP Server Skill

## Framework: FastMCP (Python)

Always use `fastmcp` — it handles the protocol boilerplate.

## Minimal Server Template

```python
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP(
    name="my-server",
    version="0.1.0",
    instructions="Describe what this server does for the LLM host.",
)

class SearchInput(BaseModel):
    query: str
    top_k: int = 5

@mcp.tool()
async def search_knowledge_base(input: SearchInput) -> list[dict]:
    """
    Search the internal knowledge base for relevant documents.
    Returns a list of {content, source, score} dicts ranked by relevance.
    Use this when you need to answer questions grounded in internal docs.
    """
    # Implementation here
    ...

if __name__ == "__main__":
    mcp.run()  # stdio transport (local)
    # mcp.run(transport="sse", port=8080)  # SSE transport (deployed)
```

## Tool Design Rules
1. Tool names must be verbs: `search_`, `create_`, `get_`, `list_`, `update_`.
2. Docstrings are the tool description seen by the LLM — write them for the model.
3. Input validation via Pydantic always. Never accept raw dicts.
4. Return structured data (list/dict), never raw strings unless unavoidable.
5. Every tool must be idempotent where possible.

## Benchmarking Template

```python
# benchmarks/bench_tools.py
import asyncio, time, statistics
from src.my_server.tools import search_knowledge_base

async def bench_search(n: int = 100):
    queries = ["test query"] * n
    latencies = []
    for q in queries:
        t0 = time.perf_counter()
        await search_knowledge_base(SearchInput(query=q))
        latencies.append((time.perf_counter() - t0) * 1000)
    print(f"p50={statistics.median(latencies):.1f}ms  "
          f"p95={statistics.quantiles(latencies, n=20)[18]:.1f}ms  "
          f"p99={sorted(latencies)[int(n*0.99)]:.1f}ms")
```

## Eval Template (LLM-as-Judge)

```python
# evals/eval_retrieval.py
CASES = [
    {"query": "...", "expected_topic": "...", "min_score": 0.8},
]

async def judge(result: list[dict], expected_topic: str) -> float:
    # Use Claude to score relevance 0.0-1.0
    ...
```

## Quality Gates
- [ ] All tools have Pydantic input models
- [ ] All tools have docstrings written for the LLM
- [ ] Benchmarks show p95 < 200ms for local tools
- [ ] At least 5 eval cases per tool with pass rate > 80%
- [ ] Server tested via `mcp dev src/server.py`
```

---

### `/skills/langgraph-agent/SKILL.md`

```markdown
---
name: langgraph-agent
description: >
  Use when building multi-agent systems or graph-based orchestration with LangGraph.
  Triggers on: LangGraph, StateGraph, agent node, graph orchestration, multi-agent,
  orchestrator agent, conditional edge, agent state.
---

# LangGraph Multi-Agent Skill

## Core Pattern: Supervisor → Specialist Graph

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str
    task_complete: bool

def supervisor_node(state: AgentState) -> AgentState:
    """Decides which specialist to route to next."""
    ...

def researcher_node(state: AgentState) -> AgentState:
    """Performs web research and adds findings to messages."""
    ...

def coder_node(state: AgentState) -> AgentState:
    """Generates or modifies code based on requirements."""
    ...

def route(state: AgentState) -> Literal["researcher", "coder", END]:
    if state["task_complete"]:
        return END
    return state["next_agent"]

graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("researcher", researcher_node)
graph.add_node("coder", coder_node)
graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route)
graph.add_edge("researcher", "supervisor")
graph.add_edge("coder", "supervisor")

app = graph.compile()
```

## Quality Gates
- [ ] State schema fully typed with TypedDict + Pydantic
- [ ] Each node is a pure function (testable in isolation)
- [ ] Graph has explicit termination condition
- [ ] Checkpointing enabled for long-running graphs (LangGraph persistence)
- [ ] Traced via LangSmith or equivalent
```

---

### `/evals/framework/runner.py` (starter)

```python
"""
Async parallel eval runner.
Usage: python -m evals.framework.runner --suite prompt_quality
"""
from __future__ import annotations
import asyncio
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Awaitable
import structlog

log = structlog.get_logger()

@dataclass
class EvalCase:
    id: str
    input: dict
    expected: dict
    metadata: dict = field(default_factory=dict)

@dataclass
class EvalResult:
    case_id: str
    score: float          # 0.0 - 1.0
    passed: bool
    latency_ms: float
    details: dict = field(default_factory=dict)

async def run_eval_suite(
    cases: list[EvalCase],
    runner_fn: Callable[[EvalCase], Awaitable[EvalResult]],
    concurrency: int = 10,
) -> list[EvalResult]:
    sem = asyncio.Semaphore(concurrency)
    async def bounded(case):
        async with sem:
            t0 = time.perf_counter()
            result = await runner_fn(case)
            result.latency_ms = (time.perf_counter() - t0) * 1000
            return result
    results = await asyncio.gather(*[bounded(c) for c in cases])
    passed = sum(1 for r in results if r.passed)
    log.info("eval_suite_complete",
             total=len(results), passed=passed,
             pass_rate=f"{passed/len(results):.1%}",
             avg_latency_ms=sum(r.latency_ms for r in results)/len(results))
    return results
```

---

### `/workflows/src/workflows/ai_pipeline_workflow.py` (starter)

```python
"""
Durable AI pipeline workflow using Temporal.io.
Demonstrates: LLM call retries, multi-step orchestration, human-in-the-loop pause.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.common import RetryPolicy

@dataclass
class PipelineInput:
    document: str
    task: str

@dataclass
class PipelineResult:
    summary: str
    critique: str
    final_output: str

# --- Activities (all I/O lives here) ---

@activity.defn
async def summarise_document(document: str) -> str:
    import anthropic
    client = anthropic.AsyncAnthropic()
    msg = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Summarise:\n\n{document}"}],
    )
    return msg.content[0].text

@activity.defn
async def critique_summary(summary: str) -> str:
    import anthropic
    client = anthropic.AsyncAnthropic()
    msg = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Critique this summary:\n\n{summary}"}],
    )
    return msg.content[0].text

# --- Workflow (deterministic orchestration only) ---

DEFAULT_RETRY = RetryPolicy(maximum_attempts=3, backoff_coefficient=2.0)
ACTIVITY_TIMEOUT = timedelta(seconds=60)

@workflow.defn
class AIPipelineWorkflow:
    @workflow.run
    async def run(self, input: PipelineInput) -> PipelineResult:
        summary = await workflow.execute_activity(
            summarise_document,
            input.document,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=DEFAULT_RETRY,
        )
        critique = await workflow.execute_activity(
            critique_summary,
            summary,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=DEFAULT_RETRY,
        )
        return PipelineResult(
            summary=summary,
            critique=critique,
            final_output=f"{summary}\n\n---\nCritique: {critique}",
        )
```

---

### `/mcp-servers/knowledge-base/src/knowledge_base/server.py` (starter)

```python
"""
Knowledge Base MCP Server.
Provides semantic search over a document corpus via ChromaDB + OpenAI/Anthropic embeddings.
Run locally: fastmcp dev src/knowledge_base/server.py
Deploy: Docker + ECS (see infra/lib/stacks/mcp-server-stack.ts)
"""
from __future__ import annotations
import os
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import chromadb
from anthropic import AsyncAnthropic

mcp = FastMCP(
    name="knowledge-base",
    version="0.1.0",
    instructions=(
        "Semantic search over the internal knowledge base. "
        "Use search_documents when answering questions that require "
        "grounding in internal documentation."
    ),
)

_client = chromadb.Client()
_collection = _client.get_or_create_collection("docs")
_anthropic = AsyncAnthropic()

class SearchInput(BaseModel):
    query: str = Field(..., description="Natural language search query")
    top_k: int = Field(5, ge=1, le=20, description="Number of results to return")

class IngestInput(BaseModel):
    content: str = Field(..., description="Document text to ingest")
    source: str = Field(..., description="Source identifier (URL, filename, etc.)")
    metadata: dict = Field(default_factory=dict)

@mcp.tool()
async def search_documents(input: SearchInput) -> list[dict]:
    """
    Semantically search the knowledge base for documents relevant to the query.
    Returns ranked list of {content, source, score} dicts.
    Use this to answer questions grounded in internal documentation.
    """
    results = _collection.query(
        query_texts=[input.query],
        n_results=input.top_k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "content": doc,
            "source": meta.get("source", "unknown"),
            "score": round(1 - dist, 4),
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]

@mcp.tool()
async def ingest_document(input: IngestInput) -> dict:
    """
    Ingest a document into the knowledge base.
    The document will be available for semantic search immediately.
    Returns {id, status}.
    """
    import hashlib
    doc_id = hashlib.sha256(f"{input.source}:{input.content}".encode()).hexdigest()[:16]
    _collection.upsert(
        ids=[doc_id],
        documents=[input.content],
        metadatas=[{"source": input.source, **input.metadata}],
    )
    return {"id": doc_id, "status": "ingested"}

if __name__ == "__main__":
    mcp.run()
```

---

### `/infra/lib/stacks/mcp-server-stack.ts` (starter)

```typescript
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as ecr from 'aws-cdk-lib/aws-ecr';

export interface McpServerStackProps extends cdk.StackProps {
  environment: 'dev' | 'staging' | 'prod';
}

export class McpServerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: McpServerStackProps) {
    super(scope, id, props);

    const repository = new ecr.Repository(this, 'McpServerRepo', {
      repositoryName: `claude-central/mcp-knowledge-base-${props.environment}`,
      removalPolicy: props.environment === 'prod'
        ? cdk.RemovalPolicy.RETAIN
        : cdk.RemovalPolicy.DESTROY,
    });

    const service = new ecsPatterns.ApplicationLoadBalancedFargateService(
      this, 'McpServerService',
      {
        taskImageOptions: {
          image: ecs.ContainerImage.fromEcrRepository(repository, 'latest'),
          containerPort: 8080,
          environment: {
            TRANSPORT: 'sse',
            PORT: '8080',
          },
          secrets: {
            // ANTHROPIC_API_KEY: ecs.Secret.fromSecretsManager(apiKeySecret),
          },
        },
        cpu: 512,
        memoryLimitMiB: 1024,
        desiredCount: props.environment === 'prod' ? 2 : 1,
      }
    );

    cdk.Tags.of(this).add('Project', 'claude-central');
    cdk.Tags.of(this).add('Environment', props.environment);
    cdk.Tags.of(this).add('Owner', 'platform-team');
  }
}
```

---

### `/.env.example`

```bash
# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# AWS
AWS_REGION=eu-west-2
AWS_PROFILE=dev

# Temporal
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default

# Observability
LANGSMITH_API_KEY=ls__...
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Vector DB
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

---

### `/pyproject.toml` (root workspace)

```toml
[tool.uv.workspace]
members = [
    "mcp-servers/knowledge-base",
    "mcp-servers/code-tools",
    "agents/orchestrator",
    "workflows",
    "evals",
    "mlops",
]

[tool.ruff]
target-version = "py312"
line-length = 100
select = ["E", "F", "I", "N", "UP", "ANN", "ASYNC", "B", "C4", "PTH", "RUF"]
ignore = ["ANN101", "ANN102"]

[tool.ruff.format]
quote-style = "double"

[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"

[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
    "integration: marks tests requiring external services",
    "eval: marks LLM quality eval tests",
    "slow: marks slow tests",
]
```

---

## Claude Code Instructions (say this after scaffolding)

Once the repo is scaffolded, establish this working pattern with Claude Code:

```
You are working inside claude-central, my AI engineering monorepo.
Always read CLAUDE.md at the start of each session.
When working in a subdirectory, also read that directory's CLAUDE.md if present.
Before starting any task, check skills/ for a matching skill and read it.
All new features require tests. All new MCP tools require evals.
```

---

## What to Build Next (Priority Order)

### Phase 1 — Foundation (Week 1-2)
1. **Complete the knowledge-base MCP server** — ChromaDB + embeddings + 5 eval cases + benchmarks. This is a deployable, demonstrable artefact.
2. **Wire up the Temporal AI pipeline** — summarise → critique → store. Shows durable compute understanding.
3. **Write eval framework** — build your own lightweight `EvalRunner` before using a framework. Demonstrates you understand what evals *are*.

### Phase 2 — Orchestration (Week 3-4)
4. **Build the LangGraph multi-agent system** — supervisor + researcher + coder + critic. Use Claude as the LLM. Adds MCP tools from Phase 1 as agent capabilities.
5. **Add MLOps pipeline** — SageMaker Pipeline + MLflow experiment tracking. Shows MLOps breadth.

### Phase 3 — Cloud & Polish (Week 5-6)
6. **CDK deploy** — get the MCP server running on Fargate. Production infra as code.
7. **Benchmark everything** — p50/p95/p99 for all MCP tools, pass rates for all eval suites. Numbers on a README are portfolio gold.
8. **Write a technical blog post** — architecture, tradeoffs, what you'd do differently. Shows communication skills.

---

## Key Technologies and Why They Matter in 2025/26

| Technology | Why Employers Care | Your Angle |
|---|---|---|
| **MCP Servers** | Becoming the standard for tool-augmented LLMs | You built, benchmarked, and deployed one |
| **LangGraph** | Replaced naive chains for production agents | Multi-agent graph with typed state |
| **Temporal.io** | Durable execution for AI pipelines (huge in prod) | LLM activities with retry/timeout handling |
| **FastMCP** | Fastest path to production MCP | Clean tool design + SSE transport |
| **Claude Code** | Agentic coding is the new IDE | Skills/context system = force multiplier |
| **AWS CDK (TypeScript)** | IaC literacy is expected at senior level | Fargate MCP server, SageMaker pipeline |
| **LLM Evals** | Every serious AI team runs evals | Custom runner + LLM-as-judge + datasets |
| **MLOps (SageMaker/MLflow)** | Bridging research → production | Experiment tracking + model registry |
| **Pydantic v2** | Type-safe AI I/O is essential | Used everywhere — models, tools, state |
| **uv** | Replacing pip/poetry — adoption is rapid | Workspace setup shows current tooling |

---

*Generated by Claude — last updated March 2026. Architecture reflects current production AI engineering patterns.*
