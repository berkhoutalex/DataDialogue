import os
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains.openai_functions import create_structured_output_runnable
from langchain_core.prompts import ChatPromptTemplate


class Step(BaseModel):
    """A step in a plan"""

    worker: str = Field(description="the name of the worker who will perform the step")
    description: str = Field(description="text of the step")

    def __str__(self):
        return f"{self.worker} - {self.description}"


class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[Step] = Field(
        description="different steps to follow, should be in sorted order"
    )

    def __str__(self):
        return "\n".join([str(s) for s in self.steps])


def planner_agent(llm):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './prompts/planner_agent_prompt.txt')
    with open(filename, "r") as f:
        planner_prompt = f.read()
    planner_prompt = ChatPromptTemplate.from_template(planner_prompt)
    planner = create_structured_output_runnable(Plan, llm, planner_prompt)

    return planner
