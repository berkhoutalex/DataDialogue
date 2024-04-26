import re


class CodeResponse:
    def __init__(self, prompt: str, raw_response: str):
        self.raw_response = raw_response
        self.code = self.extract_code()
        self.prompt = prompt
        self.extras = self.extract_extras()

    def extract_code(self):
        code2 = re.search(r"```python(.*?)```", self.raw_response, re.DOTALL)
        if code2 and code2.group(1) != "":
            return code2.group(1)
        else:
            return None

    def extract_extras(self):
        extras = (
            self.raw_response.replace("```python", "")
            .replace("```", "")
            .replace(self.code, "")
            .strip()
        )
        return extras

    def __str__(self):
        return self.raw_response

    def execute(self):
        exec(self.code)
