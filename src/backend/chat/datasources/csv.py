import os
from chat.datasources.source import Source


class CSVDataSource(Source):
    file_schemas = {}

    def __init__(self, files_path, description):
        self.files_path = files_path
        self.path_to_files_with_headers()
        self.description = description

    def path_to_files_with_headers(self):
        for file in os.listdir(self.files_path):
            if file.endswith(".csv"):
                file_path = os.path.join(self.files_path, file)
                with open(file_path, "r") as f:
                    header = f.readline()
                    header = header.replace("\n", "")
                    self.file_schemas[file_path] = header

    def file_and_headers(self, file_name):
        return f"{ file_name }: { self.file_schemas[file_name] }"

    def data_to_prompt(self):
        files = [self.file_and_headers(file) for file in self.file_schemas.keys()]
        prompt = (
            "You have access to the following files given as FileName:headers "
            + ", ".join(files)
            + f"\n The user described the data as: {self.description}"
        )
        return prompt
