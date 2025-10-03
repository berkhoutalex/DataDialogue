import os
from agentic_workflow.agents.helper import (
    Report,
    ScreenedAnswer,
    Work,
    create_structured_agent,
    make_prompt,
)
from chat.datasources.source import Source


def reporter_agent(llm):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './prompts/interface_team/reporter_agent_prompt.txt')
    with open(filename, 'r') as f:
        reporter_agent_prompt = f.read()
    return create_structured_agent(
        llm,
        Report,
        reporter_agent_prompt,
    )


def run_reporter(reporter):
    def _run_reporter(step, work: Work):
        prompt = make_prompt(step, work)

        response: Report = reporter.invoke(prompt)
        print(response)
        work.reporter_output = response

        return work

    return _run_reporter


def screener_agent(llm, data_source: Source):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './prompts/interface_team/screener_agent_prompt.txt')
    with open(filename, 'r') as f:
        screener_agent_prompt = f.read()
    
    return create_structured_agent(
        llm,
        ScreenedAnswer,
        screener_agent_prompt + f"Data Source: {data_source.data_to_prompt()}",
    )


def run_screener(original_request, screener):
    def _run_screener(step, work: Work):
        prompt = make_prompt(step, work)
        prompt["original_request"] = [original_request]
        response: ScreenedAnswer = screener.invoke(prompt)
        print(response)
        work.screener_output = response

        return work

    return _run_screener
