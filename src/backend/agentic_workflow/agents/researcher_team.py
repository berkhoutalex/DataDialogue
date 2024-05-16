from agentic_workflow.agents.helper import Work, create_agent, make_prompt
from agentic_workflow.tools.researcher import ask_user, scrape_webpages, tavily_tool
from chat.datasources.source import Source


def search_agent(llm, config):
    return create_agent(
        llm,
        [tavily_tool(config)],
        """
            You are a research assistant who can search for up-to-date info using the tavily search engine.
            Only search for information that is required to complete the request. 
            Prioritize tutorials and documentation over general search results, such as "how do i do x?" or "what is the formula for x?" and similar searches.
            You only use python, so don't search for information that requires other languages.
            Focus on looking up documentation, tutorials and equations wherever necessary.
            You MUST search for the information using the provided tool. Provide the links in your response.
            Do NOT use code that doesn't support outputting as html.
        """,
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
    return create_agent(
        llm,
        [scrape_webpages],
        """
            You are a research assistant who can scrape specified urls for more detailed information using the scrape_webpages function.
            Only search for information that is required to complete the request. 
            Prioritize tutorials and documentation over general search results.
            You only use python, so don't search for information that requires other languages.
            DO NOT attempt to code the solution.
            DO NOT attempt to source data yourself.
            Focus on looking up documentation, tutorials and equations wherever necessary.
            Trim the results to only include the most relevant information, up to a max of 1000 tokens.
            DO NOT include any code in your response and only access valid url links for search agent.
            You MUSt access the provided links. If you can't find any links in the previous message, just pass.
        """,
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
    return create_agent(
        llm,
        [ask_user],
        f"""
            You are a data scientist who is responsible for analyzing the provided data set.
            You may ask questions of the user if you need clarification on the meaning of any part of the data.
            In your response, return instructions for the coder on how to access the data required to complete the task.
            Provide specifics, such as the platform (such as sqlite, csv, etc) and information about specific tables or columns.
            Be sure to include full file paths where necessary.
            Do NOT attempt to write any code. Just describe the dataset so the coder can complete the task.
            Only include the columns and tables required to complete the request
            Data Source: {data_source.data_to_prompt()}
        """,
    )


def run_data_explorer(data_explorer):
    def _run_data_explorer(step, work: Work):
        prompt = make_prompt(step, work)

        response = data_explorer.invoke(prompt)["output"]
        print(response)
        work.data_explorer_output = response

        return work

    return _run_data_explorer