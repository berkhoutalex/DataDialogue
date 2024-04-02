from src.datadialogue.clients.client import Client
from src.datadialogue.clients.response import CodeResponse

class Conversation:
  
  def __init__(self, client:Client, max_length:int=1000):
    self.client = client
    self.max_length = max_length
    self.conversation = ""

  def add(self, response:CodeResponse):
    self.conversation += response.prompt + "\n" + response.extras + "\n"
    self.conversation = self.conversation[-self.max_length:]
    
  def run_conversation(self):
    while True:
      prompt = input("Enter your prompt: ")
      if prompt == "exit":
        break
      response = self.client.get_response(prompt)
      self.add(response)
      print(response.extras)
      exec(response.code)
    
    