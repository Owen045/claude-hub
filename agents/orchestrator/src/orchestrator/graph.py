"""LangGraph orchestration graph definition."""
from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from orchestrator.nodes import coder_node, critic_node, researcher_node, supervisor_node
from orchestrator.state import AgentState


def route(state: AgentState) -> Literal["researcher", "coder", "critic"] | str:
    """Conditional edge: route based on supervisor decision."""
    if state["task_complete"]:
        return END
    return state["next_agent"]


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("coder", coder_node)
    graph.add_node("critic", critic_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", route)
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("coder", "supervisor")
    graph.add_edge("critic", "supervisor")

    return graph


# Compiled app — import this in entrypoints
app = build_graph().compile()


async def run(task: str) -> AgentState:
    """Run the orchestration graph for a given task."""
    from langchain_core.messages import HumanMessage

    initial_state: AgentState = {
        "messages": [HumanMessage(content=task)],
        "next_agent": "researcher",
        "task": task,
        "task_complete": False,
        "iteration_count": 0,
        "research_findings": "",
        "generated_code": "",
        "critique": "",
    }
    return await app.ainvoke(initial_state)


if __name__ == "__main__":
    import asyncio

    result = asyncio.run(run("Build a Python function that fetches weather data from an API"))
    print(result["generated_code"])
