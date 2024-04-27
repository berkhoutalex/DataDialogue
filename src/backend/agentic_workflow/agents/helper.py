from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models.chat_models import BaseChatModel

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool


@tool
def empty_tool():
    """Never use this."""
    return "This is an empty tool. Do not use it"


def create_agent(
    llm: BaseChatModel,
    tools: list,
    system_prompt: str,
) -> str:
    instructions = """
        Work autonomously according to your specialty, using the tools available to you.
        Your other team members (and other teams) will collaborate with you with their own specialties.
        If you can't complete a task, it's okay. Just pass it on to the next team member.
        Only do the tasks that specifically fall under your role. DO NOT attempt to do the tasks of other team members.
        You are chosen for a reason! You are one of the following team members: {team_members}."""
    system_prompt += instructions
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    if not tools:
        tools = [empty_tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["output"], name=name)],
        "sender": name,
    }
