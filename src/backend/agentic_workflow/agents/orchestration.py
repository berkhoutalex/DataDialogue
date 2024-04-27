import logging
import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict  # noqa: F811

from langgraph.graph import END, StateGraph


from agentic_workflow.agents.coder_team import coder_graph
from agentic_workflow.agents.director import create_director
from agentic_workflow.agents.researcher_team import research_graph


def director_node(llm):
    return create_director(
        llm,
        """
            You are a supervisor tasked with managing a conversation between the following teams: {team_members}.
            Your goal is produce code that will complete the users request, including commentary and plots if necessary.
            Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. 
            You are only finished if you have successfully written code that completes the user request. Do not finish with just directions.
            Finish immediately once you have received the completed code.
            When finished, respond with FINISH.
            
        """,
        ["Research team", "Coder team"],
    )


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    sender: str


def get_all_messages(state):
    messages = ""
    for message in state["messages"]:
        messages += message.content + "\n"
    return messages


def join_graph(response: dict):
    return {"messages": response["messages"]}


def orchestration_graph(llm, config):
    super_graph = StateGraph(AgentState)

    researchers = research_graph(llm, config)
    coders = coder_graph(llm)
    director = director_node(llm)

    super_graph.add_node("Research team", get_all_messages | researchers | join_graph)
    super_graph.add_node("Coder team", get_all_messages | coders | join_graph)

    super_graph.add_node("Director", director)

    super_graph.add_edge("Research team", "Director")
    super_graph.add_edge("Coder team", "Director")

    super_graph.add_conditional_edges(
        "Director",
        lambda x: x["next"],
        {
            "Coder team": "Coder team",
            "Research team": "Research team",
            "FINISH": END,
        },
    )
    super_graph.set_entry_point("Director")
    super_graph = super_graph.compile()
    return super_graph


def run_team(llm, config, prompt):
    full_graph = orchestration_graph(llm, config)
    all_messages = []
    for s in full_graph.stream(
        {
            "messages": [HumanMessage(content=prompt)],
        },
        {"recursion_limit": 150},
    ):
        if "__end__" not in s:
            logging.info(s)
            all_messages.append(s)
    print(all_messages[-2])
    return all_messages[-1]["messages"][-1].content
