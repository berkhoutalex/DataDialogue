import re
import subprocess
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_community.llms import Ollama
import os

from agentic_workflow.agents.coder_team import reviewer_agent
from chat.datasources.source import Source


class CodeResponse:
    venv = "CodeGenVenv"

    def __init__(self, prompt: str, raw_response: str):
        self.raw_response = raw_response
        self.code = self.extract_code()
        self.dependencies = self.extract_dependencies()
        self.prompt = prompt
        self.extras = self.extract_extras()

    def extract_code(self):
        code = re.search(r"```python(.*?)```", self.raw_response, re.DOTALL)
        if code and code.group(1) != "":
            return code.group(1)
        else:
            return None

    def extract_dependencies(self):
        dependencies = re.search(r"~~~deps(.*?)~~~", self.raw_response, re.DOTALL)
        if dependencies and dependencies.group(1) != "":
            return dependencies.group(1).strip()
        else:
            return None

    def extract_extras(self):
        extras = (
            self.raw_response.replace("```python", "")
            .replace("```", "")
            .replace(self.code, "")
            .replace("~~~deps", "")
            .replace("~~~", "")
            .replace(self.dependencies, "")
            .strip()
        )
        return extras

    def __str__(self):
        return self.raw_response


def install_dependencies(codeResponse: CodeResponse):
    if "pip" in codeResponse.dependencies:
        command = f"python3 -m venv {codeResponse.venv} && .\\{codeResponse.venv}\\Scripts\\activate && {codeResponse.dependencies}"
    else:
        command = f"python3 -m venv {codeResponse.venv} && .\\{codeResponse.venv}\\Scripts\\activate && pip install {codeResponse.dependencies}"
    os.system(command)


def run_code(code, venv):
    with open("code.py", "w") as code_file:
        code_file.write(code)
    with open("code.py", "a") as code_file:
        code_file.write('\nprint("Code executed successfully")')
    command = f".\\{venv}\\Scripts\\activate && python -W ignore code.py"
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        return True, output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Status : FAIL", e.returncode, e.output)
        return False, f"Error: {e.output.decode('utf-8')}"


def run_code_response(codeResponse: CodeResponse):
    return run_code(codeResponse.code, codeResponse.venv)


def review_code(codeResponse: CodeResponse, error: str, llm, source: Source):
    reviewer = reviewer_agent(llm, source)

    prompt = f"""
        The following code was executed:
        
        {codeResponse.code}
        
        It failed with the following error:
        {error}
        
        Correct this error and return the new code.
        Return _only_ the corrected code block surrounded by ```python ```.
        Do not use any additional packages, only correct the error with the existing code.
    """

    new_code = reviewer.invoke(
        {"history": [], "step": [prompt], "team-objective": [codeResponse.prompt]}
    )["output"]
    code = re.search(r"```python(.*?)```", new_code, re.DOTALL)
    if code and code.group(1) != "":
        codeResponse.code = code.group(1)

    return codeResponse


def client_from_config(config):
    model = config.get_model_name()
    provider = config.get_model_provider()
    if provider.lower() == "openai":
        key = config.get_openai_key()
        return ChatOpenAI(
            model=model,
            api_key=key,
        )
    elif provider.lower() == "claude":
        key = config.get_claude_key()
        return ChatAnthropic(model=model, api_key=key)
    elif provider.lower() == "ollama":
        return Ollama(model=model)
