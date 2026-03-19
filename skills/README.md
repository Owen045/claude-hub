# Skills

Reusable Claude Code skill definitions. Each skill encodes hard-won patterns for a specific task category.

## How Skills Work

Before starting any task, check if a skill matches. If one does, read the corresponding `SKILL.md` before writing any code. Skills encode:
- When exactly to use this approach
- Step-by-step process
- Concrete patterns and examples
- Common mistakes to avoid
- Quality gates (done-ness criteria)

## Available Skills

| Skill | Triggers |
|---|---|
| `python-refactor` | Refactoring Python code, improving structure, extracting modules |
| `write-tests` | Writing pytest unit/integration tests |
| `aws-cdk-construct` | New CDK stack or construct, infra changes |
| `temporal-workflow` | Temporal.io workflows, activities, workers |
| `mcp-server` | MCP server, FastMCP, tool definitions, benchmarks |
| `langgraph-agent` | LangGraph, multi-agent, StateGraph, agent orchestration |
| `eval-harness` | Eval suites, LLM-as-judge, benchmark datasets |

## Creating a New Skill

1. Copy `_template/SKILL.md` to `skills/<your-skill-name>/SKILL.md`.
2. Fill in all sections — especially triggers and quality gates.
3. Add it to the table above.
