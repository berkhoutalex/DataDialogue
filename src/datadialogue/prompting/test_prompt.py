from src.datadialogue.clients.openai import OpenAI

if __name__ == "__main__":
  client = OpenAI("gpt-3.5-turbo")
  response = client.prompt("What days did AAPL experienced the largest price drop from open to close in 2020?")
  print(response.extras)
  response.execute()