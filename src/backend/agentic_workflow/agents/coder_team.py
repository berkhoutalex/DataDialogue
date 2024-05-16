from agentic_workflow.agents.helper import (
    Code,
    Dependency,
    Work,
    create_structured_agent,
    make_prompt,
)
from chat.datasources.source import Source


def coder_agent(llm, data_source: Source):
    return create_structured_agent(
        llm,
        Code,
        f"""
            You are an expert python software developer who specializes in data analysis and visualization. 
            Make sure to include the necessary imports and that the code is fully executable.
            Print out the output if you wish to provide it to the user, do not return it.
            If you came to a conclusion based on the data, make sure to print it out.
            Also print out the results of calculations performed, rather than just the final answer.
            Include only one code block surrounded only with ```python ```.  
            When rendering a plot, save it to an html file in the current directory. Do not render the plot, just save it to an html file.
            Return the completed code.
            Only code the portion of the task specified in the step.
            If there is existing code in the history, modify it to include the current step. Do not remove any existing functionality.
            Data Source: {data_source.data_to_prompt()}
        """,
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
    return create_structured_agent(
        llm,
        Code,
        f"""
            You are a software developer who specializes in reviewing code for syntax and logical errors. 
            You will look at the code provided in the last message and modify it if you believe there is something wrong.
            You do not need to run the code, just examine it for errors and make the necessary corrections.
            When rendering a plot, save it to an html file in the current directory. Do not render the plot, just save it to an html file.
            
            Data Source: {data_source.data_to_prompt()}
        """,
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
    return create_structured_agent(
        llm,
        Dependency,
        """
            You are a software developer who specializes in managing dependencies. 
            Given the block of code from either the coder or the reviewer, you must return all the dependencies required to execute it as a space-separated list.
            Only return the list of dependency names, do not include version numbers, the import phrase, pip commands or any other information.
            The dependencies should be formatted such that they can be used in a pip install command.
            You do not need to actually run the code or install the dependencies, just examine it for dependencies and supply the pip install command.
            Do not access any tools, they are not necessary.
        """,
    )


def run_dependency(dependency):
    def _run_dependency(step, work: Work):
        prompt = make_prompt(step, work)

        response: Dependency = dependency.invoke(prompt)
        print(response)
        work.dependency_output = response

        return work

    return _run_dependency
