from abc import ABC, abstractmethod

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
        },
        {
          "role": "system",
          "content": "If you need to use a specific function, please import it from specifically *src.datadialogue.sample_data.timeseries* and call it using the following syntax: `aapl_data(start_date='2020-01-01', end_date='2021-01-01')`. The available functions are: aapl_data, msft_data, goog_data, fb_data, amzn_data, tsla_data, btc_data, eth_data, doge_data, and spy_data. These are pandas dataframes with has a Date Index and Columns: High, Low, Open, Close, Volume, Adj Close."
        }
      ]
    return messages
  
  @abstractmethod
  def raw_prompt(self, prompt):
    pass
  
  def prompt(self, prompt):
    response = self.raw_prompt(prompt)
    return CodeResponse(response)
  
  