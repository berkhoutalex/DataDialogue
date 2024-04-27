import functools
import operator
from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph


from agentic_workflow.agents.helper import agent_node, create_agent
from agentic_workflow.tools.researcher import scrape_webpages, tavily_tool
from agentic_workflow.agents.director import create_director


# Research team graph state
class ResearchTeamState(TypedDict):
    # A message is added after each team member finishes
    messages: Annotated[List[BaseMessage], operator.add]
    # The team members are tracked so they are aware of
    # the others' skill-sets
    team_members: List[str]
    # Used to route work. The supervisor calls a function
    # that will update this every time it makes a decision
    next: str
    sender = "Research"


def search_agent(llm, config):
    return create_agent(
        llm,
        [tavily_tool(config)],
        """
            You are a research assistant who can search for up-to-date info using the tavily search engine.
            Only search for information that is required to complete the request. 
            DO NOT attempt to code the solution.
            DO NOT attempt to source data yourself.
            Focus on looking up documentation, tutorials and equations wherever necessary.
        
        """,
    )


def search_node(llm, config):
    return functools.partial(agent_node, agent=search_agent(llm, config), name="Search")


def research_agent(llm):
    return create_agent(
        llm,
        [scrape_webpages],
        """
            You are a research assistant who can scrape specified urls for more detailed information using the scrape_webpages function.
            Only search for information that is required to complete the request. 
            DO NOT attempt to code the solution.
            DO NOT attempt to source data yourself.
            Focus on looking up documentation, tutorials and equations wherever necessary.
            Trim the results to only include the most relevant information, up to a max of 1000 tokens.
        """,
    )


def research_node(llm):
    return functools.partial(agent_node, agent=research_agent(llm), name="WebScraper")


def director_agent(llm):
    return create_director(
        llm,
        """
            You are a supervisor tasked with managing a conversation between the following workers:  Search, WebScraper. 
            Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. 
            DO NOT attempt to code the solution.
            DO NOT attempt to source data yourself.
            Your teams objective is to provide the coding team with enough information to complete the request. 
            When finished respond with FINISH.
        """,
        ["Search", "WebScraper"],
    )


def enter_research_chain(message: str):
    results = {
        "messages": [BaseMessage(content=message)],
    }
    return results


def research_graph(llm, config):
    research_graph = StateGraph(ResearchTeamState)
    research_graph.add_node("Search", search_node(llm, config))
    research_graph.add_node("WebScraper", research_node(llm))
    research_graph.add_node("Director", director_agent(llm))

    research_graph.add_edge("Search", "Director")
    research_graph.add_edge("WebScraper", "Director")
    research_graph.add_conditional_edges(
        "Director",
        lambda x: x["next"],
        {"Search": "Search", "WebScraper": "WebScraper", "FINISH": END},
    )

    research_graph.set_entry_point("Director")
    chain = research_graph.compile()

    return enter_research_chain | chain
