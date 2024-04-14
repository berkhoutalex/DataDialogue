from io import StringIO
import json
import re
import sys

from channels.generic.websocket import WebsocketConsumer
from chat.clients.client_helper import client_from_config
from chat.datasources.csv import CSVDataSource
from chat.prompting.conversation import Conversation
import codecs


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.client = client_from_config(CSVDataSource("C:\Repos\DataDialogue\data"))
        self.conversation = Conversation(self.client)

    def disconnect(self, close_code):
        pass

    def extract_html(self, code):
        pattern = r"\b(\w+\.html)\b"
        match = re.search(pattern, code)

        if match:
            print(match.group(1))
            html_file_name = match.group(1)
            with codecs.open(html_file_name, "r", encoding="utf-8") as f:
                html_contents = f.read()

            return html_contents
        else:
            return None

    def execute_code(self, code):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(code)
        sys.stdout = old_stdout
        return redirected_output.getvalue()

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
        response = self.conversation.handle_response(message, "")
        code_output = self.execute_code(response.code)
        html = self.extract_html(response.code)
        if html:
            self.send(
                text_data=json.dumps(
                    {"html": html, "code": response.code, "message": response.extras}
                )
            )
        else:
            self.send(text_data=json.dumps({"message": response.extras}))
        if code_output and code_output != "" and code_output not in response.extras:
            self.send(
                text_data=json.dumps({"message": code_output, "code": response.code})
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if "code" in text_data_json:
            self.handleCode(text_data_json)
        else:
            self.handleMessage(text_data_json)
