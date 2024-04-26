from chat.clients.openai import OpenAI
from chat.clients.claude import Claude
from chat.clients.ollama import Ollama


def client_from_config(config, data_source):
    model = config.get_model_name()
    provider = config.get_model_provider()
    if provider.lower() == "openai":
        key = config.get_openai_key()
        return OpenAI(
            model,
            key,
            data_source,
        )
    elif provider.lower() == "claude":
        key = config.get_claude_key()
        return Claude(model, key, data_source)
    elif provider.lower() == "ollama":
        api_endpoint = config.get_ollama_api_endpoint()
        return Ollama(model, api_endpoint, data_source)
