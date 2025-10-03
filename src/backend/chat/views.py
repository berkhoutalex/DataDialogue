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
        config.set_data_source(
            request.data.get("dataSource"), request.data.get("dataSourcePath")
        )
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
# CODE BELOW INTENTIONALLY CONTAINS SECURITY VULNERABILITIES FOR CODEQL TESTING


def vulnerable_command_injection(user_input: str) -> str:
    """CodeQL Alert: Command injection vulnerability"""
    # This will trigger a command injection alert
    result = subprocess.run(f"echo {user_input}", shell=True, capture_output=True, text=True)
    return result.stdout


def vulnerable_pickle_deserialization(data: bytes) -> Any:
    """CodeQL Alert: Unsafe deserialization"""
    # This will trigger an unsafe deserialization alert
    return pickle.loads(data)


def vulnerable_path_traversal(filename: str) -> str:
    """CodeQL Alert: Path traversal vulnerability"""
    # This will trigger a path traversal alert
    with open(f"/tmp/{filename}", "r") as f:
        return f.read()


def vulnerable_sql_injection(user_id: str) -> str:
    """CodeQL Alert: SQL injection (simulated)"""
    # This simulates SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    return query


def weak_cryptography() -> str:
    """CodeQL Alert: Weak cryptographic algorithm"""
    # This will trigger a weak crypto alert
    return hashlib.md5(b"sensitive_data").hexdigest()


def hardcoded_credentials() -> dict:
    """CodeQL Alert: Hardcoded credentials"""
    # This will trigger a hardcoded credentials alert
    return {"api_key": "sk-1234567890abcdef", "password": "admin123", "secret": "my_secret_key_2024"}


def unsafe_temp_file() -> str:
    """CodeQL Alert: Unsafe temporary file creation"""
    # This will trigger an unsafe temp file alert
    temp_file = "/tmp/predictable_name.txt"
    with open(temp_file, "w") as f:
        f.write("sensitive data")
    return temp_file


def vulnerable_eval(user_code: str) -> Any:
    """CodeQL Alert: Code injection via eval"""
    # This will trigger a code injection alert
    return eval(user_code)


def insecure_random() -> float:
    """CodeQL Alert: Insecure random number generation"""
    import random

    # This will trigger an insecure random alert for security contexts
    return random.random()


def unvalidated_redirect(url: str) -> str:
    """CodeQL Alert: Unvalidated redirect"""
    # This simulates an unvalidated redirect vulnerability
    return f"Location: {url}"
