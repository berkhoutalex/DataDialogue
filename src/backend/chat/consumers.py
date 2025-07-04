import json
import re

from channels.generic.websocket import WebsocketConsumer
from agentic_workflow.agents.orchestration import run_team
from agentic_workflow.agents.helper import Work
from chat.config import Config
from agentic_workflow.helpers import (
    client_from_config,
    install_dependencies,
    run_code,
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
        output = run_code(code)
        return output

    def execute_code_response(self, code, deps):
        install_dependencies(deps)
        success, output = run_code(code)
        if success:
            return output
        else:
            return "Code failed to run with error: " + output

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
        try:
            work: Work = run_team(
                self.client, self.config, message, "", self.data_source
            )

            if not work.code_output:
                self.send(
                    text_data=json.dumps({"message": work.reporter_output.report})
                )
                return
            else:
                code = work.code_output.code
                code_output = work.code_results
                html = self.extract_html(code)
                self.send(
                    text_data=json.dumps({"message": work.reporter_output.report})
                )
                if html:
                    self.send(text_data=json.dumps({"html": html, "code": code}))
                else:
                    self.send(text_data=json.dumps({"code": code}))
                if (
                    code_output
                    and code_output != ""
                    and code_output not in work.reporter_output.report
                ):
                    self.send(
                        text_data=json.dumps({"message": code_output, "code": code})
                    )
        except Exception as e:
            import traceback

            error_message = str(e)
            tb = traceback.format_exc()
            self.send(
                text_data=json.dumps(
                    {
                        "error": "An error occurred while processing your request.",
                        "details": error_message,
                        "traceback": tb,
                    }
                )
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if "code" in text_data_json:
            self.handleCode(text_data_json)
        else:
            self.handleMessage(text_data_json)
