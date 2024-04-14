from rest_framework.decorators import api_view
from rest_framework.response import Response

from chat.config import Config


@api_view(["GET", "PATCH"])
def settings(request):
    if request.method == "GET":
        config = Config()
        settings = config.get_model_settings()
        return Response(settings)
    elif request.method == "PATCH":
        config = Config()
        config.set_model_name(request.data.get("model"))
        config.set_model_provider(request.data.get("provider"))
        if request.data.get("provider").lower() == "openai":
            config.set_openai_key(request.data.get("apiKey"))
        elif request.data.get("provider").lower() == "claude":
            config.set_claude_key(request.data.get("apiKey"))
        elif request.data.get("provider").lower() == "ollama":
            config.set_ollama_api_endpoint(request.data.get("apiKey"))
        return Response({"success": True})


@api_view(["GET"])
def key(request, model):
    config = Config()
    key = config.get_model_key(model)
    return Response({"key": key})
