import re
import subprocess
from typing import List
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_community.llms import Ollama
import os


_VENV_ = "CodeGenVenv"

def install_dependencies(deps : List[str]):
    if not deps:
        pass
    else:
        deps_str = " ".join(deps)
        command = f"python3 -m venv {_VENV_} && .\\{_VENV_}\\Scripts\\activate && pip install {deps_str}"
        os.system(command)


def run_code(code):
    with open("code.py", "w") as code_file:
        code_file.write(code)
    with open("code.py", "a") as code_file:
        code_file.write('\nprint("Code executed successfully")')
    command = f".\\{_VENV_}\\Scripts\\activate && python -W ignore code.py"
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
