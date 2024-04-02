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
          "content": "Available packages include numpy, pandas and plotly. Make sure to include the necessary imports and that the code is fully executable. Additionally, provide as much information on the math you did to get the results as possible. When rendering a plot, save it to an html file in the current directory.",
        }
      ]
    return messages
  
  @abstractmethod
  def raw_get_response(self, prompt, history = ""):
    pass
  
  def get_response(self, prompt, history = ""):
    
    response = self.raw_get_response(prompt, history)
    return CodeResponse(prompt, response)
  
  