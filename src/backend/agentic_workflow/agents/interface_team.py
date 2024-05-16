from agentic_workflow.agents.helper import (
    Report,
    ScreenedAnswer,
    Work,
    create_structured_agent,
    make_prompt,
)
from chat.datasources.source import Source


def reporter_agent(llm):
    return create_structured_agent(
        llm,
        Report,
        """
            You are a member of a data analysis team who is responsible for reporting the results of the analysis.
            In your response, provide a summary of the steps performed, the results obtained, and the conclusions drawn.
            Include any calculations performed and a summary of the steps taken.
            If there is code involved, you can assume it will provide the final results. You do not need to run the code or explain the final output.
            Only provide the final result if there is _no_ code involved.
            Make sure the response is nicely formatted and easy to read. Include line breaks where necessary.
        """,
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
    return create_structured_agent(
        llm,
        ScreenedAnswer,
        f"""
            You are a member of a data analysis team who is responsible for screening the users request and answering softballs before it returns to the entire team.
            In your response, provide an answer to the users question directly. 
            Do not use any external sources or references and do not ask for additional information.
            If you are unable to answer the question, provide a response that indicates that you are unable to answer the question.
            You may not write code in your response.
            
            Data Source: {data_source.data_to_prompt()}
        """,
    )


def run_screener(screener):
    def _run_screener(step, work: Work):
        prompt = make_prompt(step, work)

        response: ScreenedAnswer = screener.invoke(prompt)
        print(response)
        work.screener_output = response

        return work

    return _run_screener
