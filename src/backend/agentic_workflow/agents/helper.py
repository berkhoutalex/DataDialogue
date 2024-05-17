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
        description="The list of pip installable dependencies required to run the code. Should just be the package name, not the command or version number."
    )

    def __str__(self):
        return " ".join(self.dependencies)


class Code(BaseModel):
    """The result of your coding work"""

    code: str = Field(
        description="The single set of code thus far for the task. This should include all the code necessary to run the task."
    )
    description: str = Field(description="The description of the code")

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

    coder_output: Optional[Code]
    code_results: Optional[str]
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
        self.code_results = None

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
        if self.code_results:
            base_json["code_results"] = [str(self.code_results)]
        return base_json


def create_agent(
    llm: BaseChatModel,
    tools: list,
    system_prompt: str,
):
    system_prompt = system_prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="task", optional=False),
            MessagesPlaceholder(variable_name="original_request", optional=True),
            MessagesPlaceholder(variable_name="planner_output", optional=True),
            MessagesPlaceholder(variable_name="screener_output", optional=True),
            MessagesPlaceholder(variable_name="search_output", optional=True),
            MessagesPlaceholder(variable_name="research_output", optional=True),
            MessagesPlaceholder(variable_name="data_explorer_output", optional=True),
            MessagesPlaceholder(variable_name="code_output", optional=True),
            MessagesPlaceholder(variable_name="dependency_output", optional=True),
            MessagesPlaceholder(variable_name="code_results", optional=True),
            MessagesPlaceholder(variable_name="reporter_output", optional=True),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ]
    )
    if not tools:
        tools = [empty_tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)
    return executor


def create_structured_agent(llm: BaseChatModel, structure, system_prompt):
    system_prompt = system_prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="task", optional=False),
            MessagesPlaceholder(variable_name="original_request", optional=True),
            MessagesPlaceholder(variable_name="planner_output", optional=True),
            MessagesPlaceholder(variable_name="screener_output", optional=True),
            MessagesPlaceholder(variable_name="search_output", optional=True),
            MessagesPlaceholder(variable_name="research_output", optional=True),
            MessagesPlaceholder(variable_name="data_explorer_output", optional=True),
            MessagesPlaceholder(variable_name="code_output", optional=True),
            MessagesPlaceholder(variable_name="dependency_output", optional=True),
            MessagesPlaceholder(variable_name="code_results", optional=True),
            MessagesPlaceholder(variable_name="reporter_output", optional=True),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ]
    )

    agent = create_structured_output_runnable(structure, llm, prompt)

    return agent


def make_prompt(step: Step, work: Work):
    work_json = work.format_work_json()
    step_json = {"task": [step.description]}
    full_json = {**work_json, **step_json}
    return full_json
