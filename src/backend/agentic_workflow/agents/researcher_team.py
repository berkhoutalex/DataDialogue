from agentic_workflow.agents.helper import Work, create_agent, make_prompt
from agentic_workflow.tools.researcher import scrape_webpages, tavily_tool
from chat.datasources.source import Source
import os

def search_agent(llm, config):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './prompts/research_team/search_agent_prompt.txt')
    with open(filename, "r") as f:
        search_agent_prompt = f.read()
    return create_agent(
        llm,
        [tavily_tool(config)],
        search_agent_prompt,
    )


def run_search(search):
    def _run_search(step, work: Work):
        prompt = make_prompt(step, work)
        response = search.invoke(prompt)["output"]
        print(response)
        work.search_output = response

        return work

    return _run_search


def research_agent(llm):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './prompts/research_team/research_agent_prompt.txt')
    with open(filename, "r") as f:
        research_agent_prompt = f.read()
    return create_agent(
        llm,
        [scrape_webpages],
        research_agent_prompt
    )


def run_research(research):
    def _run_research(step, work: Work):
        prompt = make_prompt(step, work)

        response = research.invoke(prompt)["output"]
        print(response)
        work.research_output = response

        return work

    return _run_research


def data_explorer_agent(llm, data_source: Source):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './prompts/research_team/data_explorer_agent_prompt.txt')
    with open(filename, "r") as f:
        data_prompt = f.read()
    return create_agent(
        llm,
        [],
        data_prompt + f" Data Source: {data_source.data_to_prompt()}",
    )


def run_data_explorer(data_explorer):
    def _run_data_explorer(step, work: Work):
        prompt = make_prompt(step, work)

        response = data_explorer.invoke(prompt)["output"]
        print(response)
        work.data_explorer_output = response

        return work

    return _run_data_explorer
