from typing import Optional
from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import tool
from langchain.chains.openai_functions import create_structured_output_runnable

from agentic_workflow.agents.planner import Plan, Step
from langchain_core.pydantic_v1 import BaseModel, Field


class Dependency(BaseModel):
    """The dependencies required to run the code"""

    dependencies: list[str] = Field(
        description="The list of pip installable dependencies required to run the code"
    )
    
    def __str__(self):
        return " ".join(self.dependencies)


class Code(BaseModel):
    """The result of your coding work"""

    code: str = Field(description="The code thus far for the task")
    description: str = Field(description="Explanation of the code")
    
    def __str__(self):
        return self.code


class Report(BaseModel):
    """The result of your reporting work"""

    report: str = Field(description="The report thus far for the task")
    
    def __str__(self):
        return self.report


class ScreenedAnswer(BaseModel):
    """The result of your screening work"""

    answer: str = Field(description="The answer to the user's question")
    
    def __str__(self):
        return self.answer


@tool
def empty_tool():
    """Never use this. If you use this, you will be severely punished."""
    return "This is an empty tool. Do not use it. Do not call this tool again."


class Work:
    planner_output: Optional[Plan]
    screener_output: Optional[str]
    search_output: Optional[str]
    research_output: Optional[str]
    data_explorer_output: Optional[str]

    code_output: Optional[Code]
    dependency_output: Optional[Dependency]

    reporter_output: Optional[Report]
    def __init__(self):
        self.planner_output = None
        self.screener_output = None
        self.search_output = None
        self.research_output = None
        self.data_explorer_output = None
        self.code_output = None
        self.dependency_output = None
        self.reporter_output = None
    def format_work_json(self):
        base_json = {}
        if self.planner_output:
            base_json["planner_output"] = [str(self.planner_output)]
        if self.screener_output:
            base_json["screener_output"] = [str(self.screener_output)]
        if self.search_output:
            base_json["search_output"] = [str(self.search_output)]
        if self.research_output:
            base_json["research_output"] = [str(self.research_output)]
        if self.data_explorer_output:
            base_json["data_explorer_output"] = [str(self.data_explorer_output)]
        if self.code_output:
            base_json["code_output"] = [str(self.code_output)]
        if self.dependency_output:
            base_json["dependency_output"] = [str(self.dependency_output)]
        if self.reporter_output:
            base_json["reporter_output"] = [str(self.reporter_output)]
        return base_json


BASE_INSTRUCTION = """
        Work autonomously according to your specialty, using the tools available to you.
        If you are making a plot, save it to an html file in the current directory. Do not render the plot, just save it to an html file.
        Your team may provide you with information to help you complete your task. Be sure to use their input to improve your work.
        Your other team members will collaborate with you with their own specialties.
        If you can't complete a task, it's okay. Just pass it on to the next team member.
        Only do the tasks that specifically fall under your role. DO NOT attempt to do the tasks of other team members.
        Prioritize doing just your step well, rather than trying to do everything.
        You are chosen for a reason!"""


def create_agent(
    llm: BaseChatModel,
    tools: list,
    system_prompt: str,
):
    system_prompt = BASE_INSTRUCTION + system_prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="step", optional=False),
            MessagesPlaceholder(variable_name="planner_output", optional=True),
            MessagesPlaceholder(variable_name="screener_output", optional=True),
            MessagesPlaceholder(variable_name="search_output", optional=True),
            MessagesPlaceholder(variable_name="research_output", optional=True),
            MessagesPlaceholder(variable_name="data_explorer_output", optional=True),
            MessagesPlaceholder(variable_name="code_output", optional=True),
            MessagesPlaceholder(variable_name="dependency_output", optional=True),
            MessagesPlaceholder(variable_name="reporter_output", optional=True),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ]
    )
    if not tools:
        tools = [empty_tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def create_structured_agent(llm: BaseChatModel, structure, system_prompt):
    system_prompt = BASE_INSTRUCTION + system_prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="step", optional=False),
            MessagesPlaceholder(variable_name="planner_output", optional=True),
            MessagesPlaceholder(variable_name="screener_output", optional=True),
            MessagesPlaceholder(variable_name="search_output", optional=True),
            MessagesPlaceholder(variable_name="research_output", optional=True),
            MessagesPlaceholder(variable_name="data_explorer_output", optional=True),
            MessagesPlaceholder(variable_name="code_output", optional=True),
            MessagesPlaceholder(variable_name="dependency_output", optional=True),
            MessagesPlaceholder(variable_name="reporter_output", optional=True),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ]
    )

    agent = create_structured_output_runnable(structure, llm, prompt)

    return agent


def make_prompt(step:Step, work:Work):
    work_json = work.format_work_json()
    step_json = {"step": [step.description]}
    full_json = {**work_json, **step_json}
    return full_json
