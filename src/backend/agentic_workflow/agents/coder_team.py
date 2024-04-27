import functools
import operator
from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph


from agentic_workflow.agents.helper import agent_node, create_agent
from agentic_workflow.agents.director import create_director


class CoderTeamState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    next: str
    code: str
    sender = "Coder"


def coder_agent(llm):
    return create_agent(
        llm,
        [],
        """
            You are an expert python software developer who specializes in data analysis and visualization. 
            Available packages include numpy, sqlite, pandas and plotly. Make sure to include the necessary imports and that the code is fully executable.
            Include only one code block surrounded only with ``` ```.  
            When rendering a plot, save it to an html file in the current directory. 
            Return the completed code and the path to the saved plot.
        """,
    )


def coder_node(llm):
    return functools.partial(agent_node, agent=coder_agent(llm), name="Coder")


def reviewer_agent(llm):
    return create_agent(
        llm,
        [],
        """
            You are a software developer who specializes in reviewing code for syntax and logical errors. 
            You will look at the code provided and modify it if you identity any problems.
        """,
    )


def reviewer_node(llm):
    return functools.partial(agent_node, agent=reviewer_agent(llm), name="Reviewer")


def director_agent(llm):
    return create_director(
        llm,
        """
            You are a supervisor tasked with managing a conversation between the following workers: Coder, Reviewer. 
            Given the following user request, respond with the worker to act next. 
            Each worker will perform a task and respond with their results and status. 
            You are only finished once code is written. Return immediately once there is completed code.
            When finished, respond with FINISH.
        """,
        ["Coder", "Reviewer"],
    )


def enter_coder_chain(message: str):
    results = {
        "messages": [HumanMessage(content=message)],
    }
    return results


def coder_graph(llm):
    coder_graph = StateGraph(CoderTeamState)
    coder_graph.add_node("Coder", coder_node(llm))
    coder_graph.add_node("Reviewer", reviewer_node(llm))
    coder_graph.add_node("Director", director_agent(llm))

    coder_graph.add_edge("Coder", "Director")
    coder_graph.add_edge("Reviewer", "Director")
    coder_graph.add_conditional_edges(
        "Director",
        lambda x: x["next"],
        {"Coder": "Coder", "Reviewer": "Reviewer", "FINISH": END},
    )

    coder_graph.set_entry_point("Director")
    chain = coder_graph.compile()

    return enter_coder_chain | chain
