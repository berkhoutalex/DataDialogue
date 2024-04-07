from abc import ABC, abstractmethod

from src.datadialogue.clients.response import CodeResponse


class Client(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def code_instructions(self):
        messages = [
            {
                "role": "system",
                "content": "You are a python programmer specializing in data analysis and visualizations. Include only one code block surrounded only with the [PYTHON] [/PYTHON] tags. Make sure you check the database schema provided",
            },
            {
                "role": "system",
                "content": "Available packages include numpy, sqlite, pandas and plotly. Make sure to include the necessary imports and that the code is fully executable. When rendering a plot, save it to an html file in the current directory.",
            },
        ]
        return messages

    @abstractmethod
    def raw_get_response(self, prompt, history=""):
        pass

    def get_response(self, prompt, history=""):
        response = self.raw_get_response(prompt, history)
        return CodeResponse(prompt, response)
