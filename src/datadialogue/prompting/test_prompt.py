import pandas as pd
from src.datadialogue.datasources.sqllite import SqlLiteDataSource
from src.datadialogue.datasources.csv import CSVDataSource
from src.datadialogue.clients.openai import OpenAI

if __name__ == "__main__":
  client = OpenAI("gpt-3.5-turbo")
  data_source = SqlLiteDataSource("C:\Repos\DataDialogue\data\chinook.db")
  
  response = client.prompt("Make a cool visualization with the provided data.", data_source)
  
  
  response.execute()