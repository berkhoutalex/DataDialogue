from anthropic import Anthropic
from chat.clients.client import Client


class Claude(Client):
    def __init__(self, model, key, data_source):
        self.client = Anthropic(key)
        self.data_source = data_source
        self.model = model

    def raw_get_response(self, prompt, history):
        response = self.client.messages.create(
            max_tokens=4096,
            messages=self.code_instructions()
            + self.data_source.data_to_prompt()
            + [
                {"role": "user", "content": "Prompt:" + prompt.strip()},
                {"role": "system", "content": "History" + history},
            ],
            model=self.model,
        )

        return response.content[0].text
