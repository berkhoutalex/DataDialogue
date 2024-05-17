from agentic_workflow.agents.orchestration import run_team
from agentic_workflow.helpers import client_from_config
from chat.config import Config


def run_new(config, data_source, client):
    prompt = input("Enter your prompt: ")

    work = run_team(client, config, prompt, None, data_source)
    return work


def modify_existing_work(config, data_source, client, work):
    prompt = input("Enter your prompt: ")

    work = run_team(client, config, prompt, work.code_output, data_source)

    return work


if __name__ == "__main__":
    config = Config()
    data_source = config.get_data_source()
    client = client_from_config(config)

    work = run_new(config, data_source, client)

    print("Code executed successfully")

    while True:
        if work.code_output:
            response = input("Would you like to modify the code? (y/n): ")
            if response.lower() == "y":
                work = modify_existing_work(config, data_source, client, work)
            else:
                break
        else:
            break
