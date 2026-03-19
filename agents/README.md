# Agents

Multi-agent orchestration workflows using LangGraph.

## Architecture

```
orchestrator/    Central supervisor — routes tasks to specialists
researcher/      Web research specialist
coder/           Code generation and modification specialist
critic/          Review and evaluation specialist
```

## Pattern: Supervisor → Specialist

The orchestrator maintains shared `AgentState` and routes to specialist agents
via conditional edges. Each specialist returns results to the supervisor, which
decides the next step or terminates.

See `skills/langgraph-agent/SKILL.md` for implementation patterns.

## Running

```bash
cd agents/orchestrator
uv run python -m orchestrator.graph
```

## State Flow

```
START → supervisor → researcher → supervisor → coder → supervisor → critic → END
                  ↘ coder ↗             ↘ supervisor ↗
```
