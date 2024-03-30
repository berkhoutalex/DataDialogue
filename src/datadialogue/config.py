import toml
from os import environ

class Config:
  def __init__(self):
    self.config = toml.load("config.toml")

  def get(self, key):
    return self.config[key]
  
  def get_openai_key(self):
    return environ.get("OPENAI_API_KEY", self.config["API_KEYS"]["OPENAI"])
  
  def get_claude_key(self):
    return environ.get("ANTHROPIC_API_KEY", self.config["API_KEYS"]["CLAUDE"])

  