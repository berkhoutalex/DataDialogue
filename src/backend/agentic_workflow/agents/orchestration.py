from agentic_workflow.agents.planner import Plan, Step, planner_agent
from agentic_workflow.agents.researcher_team import (
    data_explorer_agent,
    research_agent,
    run_data_explorer,
    run_research,
    run_search,
    search_agent,
)

from agentic_workflow.agents.coder_team import (
    coder_agent,
    dependency_agent,
    reviewer_agent,
    run_coder,
    run_dependency,
    run_reviewer,
)
from agentic_workflow.agents.interface_team import (
    reporter_agent,
    run_reporter,
    run_screener,
    screener_agent,
)
from agentic_workflow.agents.helper import Work


class Team:
    def __init__(self, objective, plan, workers):
        self.plan = plan
        self.workers = workers
        self.work = Work()
        self.objective = objective

    def run_step(self, step: Step):
        worker = self.workers[step.worker]
        response = worker(step, self.work)
        print(f"Response: {response}")
        print("\n\n")
        self.work = response

    def run(self):
        for step in self.plan.steps:
            print(f"Running step: {step.description}")
            print("\n\n")
            self.run_step(step)
        return self.work


def run_team(llm, config, prompt, data_source) -> Work:
    planner = planner_agent(llm)

    seacher = search_agent(llm, config)
    researcher = research_agent(llm)
    coder = coder_agent(llm, data_source)
    reviewer = reviewer_agent(llm, data_source)
    explorer = data_explorer_agent(llm, data_source)
    dependency = dependency_agent(llm)
    screener = screener_agent(llm, data_source)
    agent_map = {
        "screener": run_screener(screener),
        "search": run_search(seacher),
        "researcher": run_research(researcher),
        "coder": run_coder(coder),
        "reviewer": run_reviewer(reviewer),
        "explorer": run_data_explorer(explorer),
        "dependencybot": run_dependency(dependency),
    }

    plan: Plan = planner.invoke(prompt)
    print(plan)
    team = Team(prompt, plan, agent_map)

    teams_answer = team.run()

    reporter = reporter_agent(llm)
    mk_report = run_reporter(reporter)
    report_step = Step(worker="reporter", description="Report the results")
    work_with_report = mk_report(report_step, teams_answer)

    return work_with_report
