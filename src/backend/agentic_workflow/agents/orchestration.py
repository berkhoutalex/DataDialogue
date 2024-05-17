from typing import Optional
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
    debugger_agent,
    dependency_agent,
    feature_developer_agent,
    reviewer_agent,
    run_coder,
    run_debugger,
    run_dependency,
    run_reviewer,
)
from agentic_workflow.agents.interface_team import (
    reporter_agent,
    run_reporter,
    run_screener,
    screener_agent,
)
from agentic_workflow.agents.helper import Code, Work
from agentic_workflow.helpers import install_dependencies, run_code


class Team:
    def __init__(self, objective, plan, workers, existing_code: Optional[Code]):
        self.plan = plan
        self.workers = workers
        self.work = Work()
        self.work.original_request = objective
        self.work.code_output = existing_code
        self.objective = objective

    def run_step(self, step: Step):
        worker = self.workers[step.worker]
        response = worker(step, self.work)
        print("\n\n")
        self.work = response

    def run_code(self):
        if self.work.code_output:
            install_dependencies(self.work.dependency_output.dependencies)
            success, output = run_code(self.work.code_output.code)
            return success, output

    def run_and_debug_code(self):
        success, output = self.run_code()
        if success:
            self.work.code_results = output
        else:
            self.work.code_results = "Code failed to run with error: " + output
            worker = self.workers["debugger"]
            step = Step(
                worker="Debugger",
                description="The provided code failed to run. Attempt to correct the error.",
            )
            response = worker(step, self.work)
            self.work = response
            success, output = self.run_code()
            self.work.code_results = output

        return output

    def run(self):
        for step in self.plan.steps:
            print(f"Running step: {step.description}")
            print("\n\n")
            self.run_step(step)
        if self.work.code_output:
            self.run_and_debug_code()

        return self.work


def run_team(llm, config, prompt, existing_code, data_source) -> Work:
    planner = planner_agent(llm)
    if existing_code:
        prompt = prompt + "\n\n" + "Existing code: \n" + existing_code.code
    plan: Plan = planner.invoke(prompt)
    print(plan)

    seacher = search_agent(llm, config)
    researcher = research_agent(llm)
    coder = coder_agent(llm, data_source)
    feature_dev = feature_developer_agent(llm, data_source)
    reviewer = reviewer_agent(llm, data_source)
    explorer = data_explorer_agent(llm, data_source)
    dependency = dependency_agent(llm)
    screener = screener_agent(llm, data_source)
    debugger = debugger_agent(llm)
    agent_map = {
        "screener": run_screener(prompt, screener),
        "search": run_search(seacher),
        "researcher": run_research(researcher),
        "coder": run_coder(coder),
        "feature_developer": run_coder(feature_dev),
        "reviewer": run_reviewer(reviewer),
        "explorer": run_data_explorer(explorer),
        "dependencybot": run_dependency(dependency),
        "debugger": run_debugger(debugger),
    }

    team = Team(prompt, plan, agent_map, existing_code)

    teams_answer = team.run()

    reporter = reporter_agent(llm)
    mk_report = run_reporter(reporter)
    report_step = Step(worker="reporter", description="Report the results")
    work_with_report = mk_report(report_step, teams_answer)

    return work_with_report
