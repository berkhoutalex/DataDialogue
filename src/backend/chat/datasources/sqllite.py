import sqlite3

from chat.datasources.source import Source


class SqlLiteDataSource(Source):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connect()
        self.schema = self.get_schema()

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def execute(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_schema(self):
        self.connect()
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_table_schema(self, table_name: str):
        query = f"PRAGMA table_info('{table_name}');"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def table_to_string(self, table_name: str):
        schema = self.get_table_schema(table_name)
        return (
            table_name
            + ": {"
            + ", ".join([col[1] + ":" + col[2] for col in schema])
            + "}"
        )

    def data_to_prompt(self):
        return [
            {
                "role": "system",
                "content": "You have access to a sqllite database located at "
                + self.db_path
                + " with the following schema - "
                + ", ".join([self.table_to_string(table[0]) for table in self.schema]),
            }
        ]
