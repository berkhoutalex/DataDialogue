import ollama

from chat.clients.client import Client


class Ollama(Client):
    def __init__(self, model, key, data_source):
        self.data_source = data_source
        self.client = ollama.Client(key)
        self.model = model

    def raw_get_response(self, prompt, history):
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
