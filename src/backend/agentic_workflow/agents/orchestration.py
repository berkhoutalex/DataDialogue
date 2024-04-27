from agentic_workflow.agents.planner import Plan, Step, planner_agent
from agentic_workflow.agents.researcher_team import (
    data_explorer_agent,
    research_agent,
    search_agent,
)

from langchain.agents import (
    AgentExecutor,
)

from agentic_workflow.agents.coder_team import (
    coder_agent,
    dependency_agent,
    reviewer_agent,
)


class Team:
    def __init__(self, objective, plan, workers):
        self.plan = plan
        self.workers = workers
        self.history = []
        self.objective = objective

    def format_history_and_step_in_prompt(self, step: Step):
        return {
            "step": [step.description],
            "team-objective": [self.objective],
            "history": self.history,
        }

    def run_step(self, step: Step):
        worker: AgentExecutor = self.workers[step.worker]
        prompt = self.format_history_and_step_in_prompt(step)
        response = worker.invoke(prompt)["output"]
        print(f"Response: {response}")
        print("\n\n")
        self.history.append(step.worker + ":" + response)

    def run(self):
        for step in self.plan.steps:
            print(f"Running step: {step.description}")
            print("\n\n")
            self.run_step(step)
        return self.history[-1]


def run_team(llm, config, prompt, data_source):
    planner = planner_agent(llm)

    seacher = search_agent(llm, config)
    researcher = research_agent(llm)
    coder = coder_agent(llm, data_source)
    reviewer = reviewer_agent(llm, data_source)
    explorer = data_explorer_agent(llm, data_source)
    dependency = dependency_agent(llm)
    agent_map = {
        "search": seacher,
        "researcher": researcher,
        "coder": coder,
        "reviewer": reviewer,
        "explorer": explorer,
        "dependencybot": dependency,
    }

    plan: Plan = planner.invoke(prompt)
    print(plan)
    team = Team(prompt, plan, agent_map)

    return team.run()
