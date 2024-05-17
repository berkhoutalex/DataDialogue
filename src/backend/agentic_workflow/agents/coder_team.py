import os
from agentic_workflow.agents.helper import (
    Code,
    Dependency,
    Work,
    create_agent,
    create_structured_agent,
    make_prompt,
)
from chat.datasources.source import Source


def coder_agent(llm, data_source: Source):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "./prompts/coder_team/coder_agent_prompt.txt")
    with open(filename, "r") as f:
        coder_agent_prompt = f.read()
    return create_structured_agent(
        llm,
        Code,
        coder_agent_prompt + f"Data Source: {data_source.data_to_prompt()}",
    )


def feature_developer_agent(llm, data_source: Source):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, "./prompts/coder_team/feature_developer_agent_prompt.txt"
    )
    with open(filename, "r") as f:
        coder_agent_prompt = f.read()
    return create_structured_agent(
        llm,
        Code,
        coder_agent_prompt + f" Data Source: {data_source.data_to_prompt()}",
    )


def run_coder(coder):
    def _run_coder(step, work: Work):
        prompt = make_prompt(step, work)

        response: Code = coder.invoke(prompt)
        print(response)
        work.code_output = response

        return work

    return _run_coder


def reviewer_agent(llm, data_source: Source):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "./prompts/coder_team/reviewer_agent_prompt.txt")
    with open(filename, "r") as f:
        reviewer_agent_prompt = f.read()

    return create_structured_agent(
        llm,
        Code,
        reviewer_agent_prompt + f" Data Source: {data_source.data_to_prompt()}",
    )


def run_reviewer(reviewer):
    def _run_reviewer(step, work: Work):
        prompt = make_prompt(step, work)

        response: Code = reviewer.invoke(prompt)
        print(response)
        work.code_output = response

        return work

    return _run_reviewer


def dependency_agent(llm):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "./prompts/coder_team/dependency_agent_prompt.txt")
    with open(filename, "r") as f:
        dependency_agent_prompt = f.read()
    return create_agent(
        llm,
        [],
        dependency_agent_prompt,
    )


def run_dependency(dependency):
    def _run_dependency(step, work: Work):
        prompt = make_prompt(step, work)

        response: Dependency = dependency.invoke(prompt)
        deps = response["output"].split(",")
        deps = Dependency(dependencies=deps)
        print(deps)
        work.dependency_output = deps

        return work

    return _run_dependency


def debugger_agent(llm):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "./prompts/coder_team/debugger_agent_prompt.txt")
    with open(filename, "r") as f:
        coder_agent_prompt = f.read()
    return create_structured_agent(
        llm,
        Code,
        coder_agent_prompt,
    )


def run_debugger(debugger):
    def _run_debugger(step, work: Work):
        prompt = make_prompt(step, work)
        response: Code = debugger.invoke(prompt)
        print(response)
        work.code_output = response

        return work

    return _run_debugger
