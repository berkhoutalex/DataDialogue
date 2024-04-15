import toml
from os import environ

from chat.datasources.csv import CSVDataSource
from chat.datasources.sqlite import SqliteDataSource


class Config:
    def __init__(self):
        self.config = toml.load("config.toml")

    def get(self, key):
        return self.config[key]

    def get_openai_key(self):
        return environ.get("OPENAI_API_KEY", self.config["API_KEYS"]["OPENAI"])

    def get_claude_key(self):
        return environ.get("ANTHROPIC_API_KEY", self.config["API_KEYS"]["CLAUDE"])

    def get_ollama_api_endpoint(self):
        return self.config["API_KEYS"]["OLLAMA"]

    def get_model_name(self):
        return self.config["MODEL"]["model"]

    def get_model_provider(self):
        return self.config["MODEL"]["provider"]

    def set(self, key1, key2, value):
        self.config[key1][key2] = value
        toml.dump(self.config, open("config.toml", "w"))

    def set_openai_key(self, value):
        self.set("API_KEYS", "OPENAI", value)

    def set_claude_key(self, value):
        self.set("API_KEYS", "CLAUDE", value)

    def set_ollama_api_endpoint(self, value):
        self.set("API_KEYS", "OLLAMA", value)

    def set_model_name(self, value):
        self.set("MODEL", "model", value)

    def set_model_provider(self, value):
        self.set("MODEL", "provider", value)

    def get_model_settings(self):
        if self.get_model_provider().lower() == "openai":
            key = self.get_openai_key()
        elif self.get_model_provider().lower() == "anthropic":
            key = self.get_claude_key()
        elif self.get_model_provider().lower() == "ollama":
            key = self.get_ollama_api_endpoint()
        return {
            "model": self.get_model_name(),
            "provider": self.get_model_provider(),
            "key": key,
            "dataSource": self.config["DATA_SOURCE"]["source_type"],
            "dataSourcePath": self.config["DATA_SOURCE"]["source_path"],
        }

    def get_model_key(self, model):
        if model.lower() == "openai":
            return self.get_openai_key()
        elif model.lower() == "anthropic":
            return self.get_claude_key()
        elif model.lower() == "ollama":
            return self.get_ollama_api_endpoint()
        return None

    def get_data_source(self):
        source_type = self.config["DATA_SOURCE"]["source_type"]
        if source_type == "csv":
            return CSVDataSource(self.config["DATA_SOURCE"]["source_path"])
        elif source_type == "sqlite":
            return SqliteDataSource(self.config["DATA_SOURCE"]["source_path"])

    def set_data_source(self, source_type, source_path):
        self.set("DATA_SOURCE", "source_type", source_type)
        self.set("DATA_SOURCE", "source_path", source_path)
