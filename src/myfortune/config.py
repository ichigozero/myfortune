import os
import json
from pathlib import Path

DEFAULT_CONFIG_PATH = os.path.join(str(Path.home()), '.myfortune.json')


class AppConfig:
    def __init__(self, config_path=''):
        self._config_path = config_path or DEFAULT_CONFIG_PATH
        self._config_values = None

    def export_config(self):
        with open(self._config_path, 'w') as file:
            file.write(
                json.dumps(
                    self._config_values,
                    indent=2,
                    sort_keys=True
                )
            )

    def import_config(self):
        try:
            with open(self._config_path, 'r') as file:
                self._config_values = json.load(file)
        except OSError:
            pass
