from chat.clients.client import Client
from chat.clients.response import CodeResponse


class Conversation:
    def __init__(self, client: Client, max_length: int = 1000):
        self.client = client
        self.max_length = max_length
        self.conversation = ""

    def add(self, response: CodeResponse):
        self.conversation += response.prompt + "\n" + response.extras + "\n"
        self.conversation = self.conversation[-self.max_length :]

    def handle_response(self, prompt: str, history: str):
        response = self.client.get_response(prompt, history)
        self.add(response)
        return response

    def run_conversation(self):
        while True:
            prompt = input("Enter your prompt: ")
            if prompt == "exit":
                break
            response = self.client.get_response(prompt)
            self.add(response)
            print(response.extras)
            exec(response.code)
