from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains.openai_functions import create_structured_output_runnable
from langchain_core.prompts import ChatPromptTemplate


class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

    def __str__(self):
        return "\n".join(self.steps)


def planner_agent(llm):
    planner_prompt = ChatPromptTemplate.from_template(
        """
          For the given objective, come up with a simple step by step plan.
          This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps.
          The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.
          To complete the steps, you have access to a research team, which will search the web for additional information 
          and a coder team, which will write code to solve the problem.
          The research team consists of a search agent and a web scraper agent.
          The coder team consists of a coder agent and a reviewer agent.
          {objective}
        """
    )
    planner = create_structured_output_runnable(Plan, llm, planner_prompt)

    return planner
