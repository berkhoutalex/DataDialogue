import ollama

from src.datadialogue.clients.client import Client
from src.datadialogue.config import Config


class Ollama(Client):
    def __init__(self, model, data_source):
        config = Config()
        self.data_source = data_source
        self.client = ollama.Client(config.get_ollama_api_endpoint())
        self.model = model

    def raw_get_response(self, prompt, history):
        print(self.code_instructions() + self.data_source.data_to_prompt())
        response = self.client.chat(
            messages=self.code_instructions()
            + self.data_source.data_to_prompt()
            + [
                {"role": "user", "content": "Prompt:" + prompt.strip()},
                {"role": "system", "content": "History" + history},
            ],
            model=self.model,
        )

        return response["message"]["content"]
