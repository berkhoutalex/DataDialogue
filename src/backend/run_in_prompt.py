from agentic_workflow.agents.orchestration import run_team
from agentic_workflow.helpers import client_from_config
from chat.config import Config


if __name__ == "__main__":
    config = Config()
    data_source = config.get_data_source()
    client = client_from_config(config)
    prompt = input("Enter your prompt: ")

    work = run_team(client, config, prompt, data_source)
