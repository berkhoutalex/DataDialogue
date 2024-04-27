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
    planner_prompt = ChatPromptTemplate.from_template(
        """
            For the given objective, come up with a simple step by step plan.
            This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps.
            The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.
            You have access to the following agents to perform steps:
                explorer - analyzes the provided dataset and provides directions on how to access the required data
                search - comes up with urls to search for information. This agent is useful for finding code documentation, tutorials and formulas.
                researcher - Uses the urls provided by the search agent to find even more detailed information to provide to the coder. Should be used after the search agent.
                coder - writes the requested code
                dependencybot - creates a list of python dependecies used by the code. You must always use this bot and it must go last in the plan.
            {objective}
        """
    )
    planner = create_structured_output_runnable(Plan, llm, planner_prompt)

    return planner
