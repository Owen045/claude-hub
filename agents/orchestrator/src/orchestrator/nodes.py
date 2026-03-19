"""Agent node definitions for the orchestration graph."""
from __future__ import annotations

import structlog
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from orchestrator.prompts import (
    CODER_PROMPT,
    CRITIC_PROMPT,
    RESEARCHER_PROMPT,
    SUPERVISOR_PROMPT,
)
from orchestrator.state import AgentState

log = structlog.get_logger()

MAX_ITERATIONS = 10

_llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)


def supervisor_node(state: AgentState) -> AgentState:
    """
    Supervisor: reviews current state and routes to the next specialist,
    or marks the task complete.
    """
    if state["iteration_count"] >= MAX_ITERATIONS:
        log.warning("max_iterations_reached", count=state["iteration_count"])
        return {"task_complete": True, "iteration_count": state["iteration_count"] + 1}

    messages = [
        SystemMessage(content=SUPERVISOR_PROMPT),
        *state["messages"],
        HumanMessage(content=f"Current task: {state['task']}\nWhat should happen next?"),
    ]
    response = _llm.invoke(messages)
    content = str(response.content).strip().lower()

    next_agent = "researcher"
    task_complete = False

    if "finish" in content:
        task_complete = True
    elif "coder" in content:
        next_agent = "coder"
    elif "critic" in content:
        next_agent = "critic"

    log.info("supervisor_decision", next_agent=next_agent, task_complete=task_complete)
    return {
        "messages": [response],
        "next_agent": next_agent,
        "task_complete": task_complete,
        "iteration_count": state["iteration_count"] + 1,
    }


def researcher_node(state: AgentState) -> AgentState:
    """Researcher: gathers information and returns structured findings."""
    messages = [
        SystemMessage(content=RESEARCHER_PROMPT),
        *state["messages"],
    ]
    response = _llm.invoke(messages)
    log.info("researcher_complete")
    return {
        "messages": [response],
        "research_findings": str(response.content),
    }


def coder_node(state: AgentState) -> AgentState:
    """Coder: writes or modifies code to complete the task."""
    messages = [
        SystemMessage(content=CODER_PROMPT),
        *state["messages"],
        HumanMessage(content=f"Research findings:\n{state.get('research_findings', 'None')}"),
    ]
    response = _llm.invoke(messages)
    log.info("coder_complete")
    return {
        "messages": [response],
        "generated_code": str(response.content),
    }


def critic_node(state: AgentState) -> AgentState:
    """Critic: reviews the generated code and provides feedback."""
    code = state.get("generated_code", "No code generated yet.")
    messages = [
        SystemMessage(content=CRITIC_PROMPT),
        *state["messages"],
        HumanMessage(content=f"Please review this code:\n\n{code}"),
    ]
    response = _llm.invoke(messages)
    log.info("critic_complete")
    return {
        "messages": [response],
        "critique": str(response.content),
    }
