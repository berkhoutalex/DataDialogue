from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import tool


@tool
def empty_tool():
    """Never use this. If you use this, you will be severely punished."""
    return "This is an empty tool. Do not use it. Do not call this tool again."


def create_agent(
    llm: BaseChatModel,
    tools: list,
    system_prompt: str,
) -> str:
    instructions = """
        Work autonomously according to your specialty, using the tools available to you.
        If you are making a plot, save it to an html file in the current directory. Do not render the plot, just save it to an html file.
        Your team may provide you with information to help you complete your task. Be sure to use their input to improve your work.
        Your other team members (and other teams) will collaborate with you with their own specialties.
        If you can't complete a task, it's okay. Just pass it on to the next team member.
        Only do the tasks that specifically fall under your role. DO NOT attempt to do the tasks of other team members.
        Prioritize doing just your step well, rather than trying to do everything.
        You are chosen for a reason!"""
    system_prompt += instructions
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="history"),
            MessagesPlaceholder(variable_name="step"),
            MessagesPlaceholder(variable_name="team-objective"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    if not tools:
        tools = [empty_tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor
