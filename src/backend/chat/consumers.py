import json
import re

from channels.generic.websocket import WebsocketConsumer
from agentic_workflow.agents.orchestration import run_team
from chat.config import Config
from agentic_workflow.helpers import (
    CodeResponse,
    client_from_config,
    install_dependencies,
    run_code,
    review_code,
    run_code_response,
)
import codecs


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        config = Config()
        self.config = config
        data_source = config.get_data_source()
        self.data_source = data_source
        self.client = client_from_config(config)

    def disconnect(self, close_code):
        pass

    def extract_html(self, code):
        pattern = r"\b(\w+\.html)\b"
        match = re.search(pattern, code)

        if match:
            html_file_name = match.group(1)
            with codecs.open(html_file_name, "r", encoding="utf-8") as f:
                html_contents = f.read()

            return html_contents
        else:
            return None

    def execute_code(self, code: str):
        output = run_code(code, CodeResponse.venv)
        return output

    def execute_code_response(self, code_response: CodeResponse):
        install_dependencies(code_response)
        success, output = run_code_response(code_response)
        if success:
            return output
        else:
            new_code_response = review_code(
                code_response, output, self.client, self.data_source
            )
            install_dependencies(new_code_response)
            success, output = run_code_response(new_code_response)
            return output

    def handleCode(self, text_data_json):
        code = text_data_json["code"]
        code_output = self.execute_code(code)
        html = self.extract_html(code)
        output = {"code": code}
        if html:
            output["html"] = html
        if code_output and code_output != "":
            output["message"] = code_output
        self.send(text_data=json.dumps(output))

    def handleMessage(self, text_data_json):
        message = text_data_json["message"]

        report, response, history = run_team(
            self.client, self.config, message, self.data_source
        )
        response = CodeResponse(message, response)
        if response.code is None:
            self.send(text_data=json.dumps({"message": report}))
            return
        else:
            code_output = self.execute_code_response(response)
            html = self.extract_html(response.code)
            self.send(text_data=json.dumps({"message": report}))
            if html:
                self.send(text_data=json.dumps({"html": html, "code": response.code}))
            else:
                self.send(text_data=json.dumps({"code": response.code}))
            if code_output and code_output != "" and code_output not in response.extras:
                self.send(
                    text_data=json.dumps(
                        {"message": code_output, "code": response.code}
                    )
                )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if "code" in text_data_json:
            self.handleCode(text_data_json)
        else:
            self.handleMessage(text_data_json)
