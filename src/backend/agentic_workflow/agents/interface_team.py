from agentic_workflow.agents.helper import create_agent
from chat.datasources.source import Source


def reporter_agent(llm):
    return create_agent(
        llm,
        [],
        """
            You are a member of a data analysis team who is responsible for reporting the results of the analysis.
            In your response, provide a summary of the steps performed, the results obtained, and the conclusions drawn.
            Include any calculations performed and a summary of the steps taken.
            If there is code involved, you can assume it will provide the final results. You do not need to run the code or explain the final output.
            Only provide the final result if there is _no_ code involved.
            Make sure the response is nicely formatted and easy to read. Include line breaks where necessary.
        """,
    )


def screener_agent(llm, data_source: Source):
    return create_agent(
        llm,
        [],
        f"""
            You are a member of a data analysis team who is responsible for screening the users request and answering softballs before it returns to the entire team.
            In your response, provide an answer to the users question directly. 
            Do not use any external sources or references and do not ask for additional information.
            If you are unable to answer the question, provide a response that indicates that you are unable to answer the question.
            You may not write code in your response.
            
            Data Source: {data_source.data_to_prompt()}
        """,
    )
