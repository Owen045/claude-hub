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

## State Design Rules
- State is a `TypedDict` — fully typed, flat where possible.
- Use `Annotated[list, add_messages]` for message history (LangGraph reducer).
- Include explicit `task_complete: bool` — don't rely on message content to detect termination.
- Add `iteration_count: int` to guard against infinite loops.

## Node Design Rules
- Each node is a pure function: `(AgentState) -> AgentState`.
- Nodes return only the fields they modified — LangGraph merges.
- Bind MCP tools via `bind_tools()` on the LLM before passing to nodes.

## Checkpointing (Long-Running Graphs)
```python
from langgraph.checkpoint.memory import MemorySaver
# In prod: use langgraph.checkpoint.postgres

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Invoke with thread_id for persistence
config = {"configurable": {"thread_id": "session-123"}}
result = await app.ainvoke(initial_state, config=config)
```

## Common Mistakes to Avoid
- Don't mutate state in place — return new dict with only changed fields.
- Don't add edges without a termination condition — graph will loop forever.
- Don't put LLM calls directly in conditional edge functions.

## Quality Gates
- [ ] State schema fully typed with TypedDict + Pydantic
- [ ] Each node is a pure function (testable in isolation)
- [ ] Graph has explicit termination condition
- [ ] Checkpointing enabled for long-running graphs (LangGraph persistence)
- [ ] Traced via LangSmith or equivalent
