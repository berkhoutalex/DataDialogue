import os
from chat.config import Config
from agentic_workflow.agents.orchestration import run_team
from langchain_openai.chat_models import ChatOpenAI


if __name__ == "__main__":
    config = Config()
    os.environ["TAVILY_API_KEY"] = config.get_tavily_api_key()
    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=config.get_openai_key())

    prompt = "Write code to make a graph of a aapl stock prices over the last year."
    run_team(llm, config, prompt)
