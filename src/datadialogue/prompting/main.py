from src.datadialogue.clients.openai import OpenAI
from src.datadialogue.prompting.conversation import Conversation
from src.datadialogue.datasources.sqllite import SqlLiteDataSource

if __name__ == "__main__":
    data_source = SqlLiteDataSource("C:\Repos\DataDialogue\data\chinook.db")
    client = OpenAI("gpt-3.5-turbo-0125", data_source)
    convo = Conversation(client)

    convo.run_conversation()
