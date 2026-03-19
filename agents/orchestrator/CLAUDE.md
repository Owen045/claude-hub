# Orchestrator Agent — Sub-Agent Context

This CLAUDE.md extends (not overrides) the root CLAUDE.md.
Read the root CLAUDE.md first, then this file.

## This Directory
LangGraph-based multi-agent orchestration system.
The orchestrator is the supervisor node that routes to specialist agents.

## Key Files
- `src/orchestrator/graph.py` — StateGraph definition, edge wiring
- `src/orchestrator/nodes.py` — Node functions (supervisor, specialist calls)
- `src/orchestrator/state.py` — AgentState TypedDict
- `src/orchestrator/prompts.py` — System prompts per agent role

## Conventions
- State must remain a flat TypedDict — no nested mutable objects.
- Every node function is a pure function: `(AgentState) -> AgentState`.
- Include `iteration_count` in state and assert `< MAX_ITERATIONS` to prevent loops.
- Use `langsmith` tracing — set `LANGCHAIN_TRACING_V2=true` in `.env`.

## Relevant Skill
Read `skills/langgraph-agent/SKILL.md` before making any changes here.
