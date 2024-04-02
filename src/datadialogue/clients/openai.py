import json
import os
from openai import OpenAI as OA
from src.datadialogue.datasources.source import Source
from src.datadialogue.clients.client import Client
from src.datadialogue.config import Config

class OpenAI(Client):
  def __init__(self, model, data_source):
    config = Config()
    self.data_source = data_source
    api_key = config.get_openai_key()
    self.client = OA(api_key=api_key)
    self.model = model
    
  def raw_get_response(self, prompt, history):
    response = self.client.chat.completions.create(
      messages=self.code_instructions() + self.data_source.data_to_prompt() + [{"role": "user", "content": "Prompt:" + prompt.strip()}, {"role": "system", "content": "History"+history}],
      model=self.model,
    )

    return response.choices[0].message.content

  