from abc import ABC, abstractmethod

from src.datadialogue.datasources.source import Source
from src.datadialogue.clients.response import CodeResponse
class Client(ABC):
  
  @abstractmethod
  def __init__(self):
    pass
  
  def code_instructions(self):
    messages = [
        {
          "role": "system", 
          "content": "You are a python programmer specializing in data analysis and visualizations. Do not try to source the data yourself, use the tools provided. Include the code in your response, surrounded by triple backticks",
        },
        {
          "role": "system", 
          "content": "Available packages include numpy, pandas, matplotlib and plotly. Make sure to include the necessary imports and that the code is fully executable. Additionally, provide as much information on the math you did to get the results as possible.",
        }
      ]
    return messages
  
  @abstractmethod
  def raw_prompt(self, prompt, data_source: Source):
    pass
  
  def prompt(self, prompt, data_source: Source):
    
    response = self.raw_prompt(prompt, data_source)
    return CodeResponse(response)
  
  