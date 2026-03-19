"""Shared state schema for the multi-agent graph."""
from __future__ import annotations

from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Shared state passed between all nodes in the orchestration graph."""

    # Message history — uses LangGraph's add_messages reducer (append-only)
    messages: Annotated[list, add_messages]

    # Routing: which specialist the supervisor selected
    next_agent: str

    # Task lifecycle
    task: str
    task_complete: bool
    iteration_count: int

    # Accumulated outputs from specialists
    research_findings: str
    generated_code: str
    critique: str
