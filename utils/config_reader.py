import configparser
import os


class ConfigReader:
    _config = None

    @classmethod
    def _load(cls):
        if cls._config is None:
            cls._config = configparser.RawConfigParser()
            config_path = os.path.join(
                os.path.dirname(__file__), '..', 'config', 'config.properties'
            )
            # configparser needs a section header; wrap the file
            with open(os.path.abspath(config_path), 'r') as f:
                content = '[DEFAULT]\n' + f.read()
            cls._config.read_string(content)

    @classmethod
    def get(cls, key: str) -> str:
        cls._load()
        return cls._config['DEFAULT'].get(key, '')
