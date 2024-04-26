from openai import OpenAI as OA
from chat.clients.client import Client


class OpenAI(Client):
    def __init__(self, model, key, data_source):
        self.data_source = data_source
        api_key = key
        self.client = OA(api_key=api_key)
        self.model = model

    def raw_get_response(self, prompt, history):
        response = self.client.chat.completions.create(
            messages=self.code_instructions()
            + self.data_source.data_to_prompt()
            + [
                {"role": "user", "content": "Prompt:" + prompt.strip()},
                {"role": "system", "content": "History" + history},
            ],
            model=self.model,
        )

        return response.choices[0].message.content
