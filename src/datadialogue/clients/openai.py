import json
import os
from openai import OpenAI as OA
from src.datadialogue.datasources.source import Source
from src.datadialogue.clients.client import Client
from src.datadialogue.config import Config

class OpenAI(Client):
  def __init__(self, model):
    config = Config()
    
    api_key = config.get_openai_key()
    self.client = OA(api_key=api_key)
    self.model = model
    
  def raw_prompt(self, prompt, data_source: Source):
    response = self.client.chat.completions.create(
      messages=self.code_instructions() + data_source.data_to_prompt() + [{"role": "user", "content": prompt.strip()}],
      model=self.model,
    )

    return response.choices[0].message.content

  