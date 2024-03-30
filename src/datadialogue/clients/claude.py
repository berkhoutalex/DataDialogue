import os
from anthropic import Anthropic
from src.datadialogue.clients.client import Client
from src.datadialogue.config import Config

class Claude(Client):
  def __init__(self, model):
    config = Config()
    api_key = config.get_claude_key()
    self.client = Anthropic(api_key)
    self.model = model
    
  def raw_prompt(self, prompt):
    response = self.client.messages.create(
      max_tokens=4096,
      messages=self.code_instructions() + [{"role": "user", "content": prompt.strip()}],
      model=self.model
    )
    
    return response.content[0].text
