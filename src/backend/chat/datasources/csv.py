import os
from chat.datasources.source import Source
import pandas as pd


class CSVDataSource(Source):
    file_schemas = {}

    def __init__(self, files_path, description):
        self.files_path = files_path
        self.path_to_file_dtypes()
        self.description = description

    def file_and_headers(self, file_name):
        return f"{ file_name }: { self.file_schemas[file_name] }"

    def path_to_file_dtypes(self):
        for file in os.listdir(self.files_path):
            if file.endswith(".csv"):
                file_path = os.path.join(self.files_path, file)
                with open(file_path, "r") as f:
                    csv = pd.read_csv(f)
                    dtypes = csv.dtypes
                    self.file_schemas[file_path] = dtypes

    def file_and_dtypes(self, file_name):
        return f"{ file_name }:\n { self.file_dtypes[file_name].values() }"

    def data_to_prompt(self):
        files = [self.file_and_headers(file) for file in self.file_schemas.keys()]

        prompt = (
            "You have access to the following files given as FileName:\nheader   dtype "
            + ",\n ".join(files)
            + f"\n The user described the data as: {self.description}"
        )
        return prompt
