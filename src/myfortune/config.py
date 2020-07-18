import os
import json
from pathlib import Path

DEFAULT_CONFIG_PATH = os.path.join(str(Path.home()), 'myfortune.json')


class AppConfig:
    def __init__(self):
        self._config_path = DEFAULT_CONFIG_PATH
        self._config_values = None

    def import_config(self):
        try:
            with open(self._config_path, 'r') as file:
                self._config_values = json.load(file)
        except OSError:
            pass
