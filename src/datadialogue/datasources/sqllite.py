
import sqlite3

from src.datadialogue.datasources.source import Source


class SqlLiteDataSource(Source):
    def __init__(self, db_path: str):
        self.db_path = db_path

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
      
    def data_to_prompt(self):
      schema = self.get_schema()
      return [
        {
          "role": "system",
          "content": "You have access to a sqllite database located at " + self.db_path + " with the following schema " + ", ".join([table[0] for table in schema])
        }
      ]
          