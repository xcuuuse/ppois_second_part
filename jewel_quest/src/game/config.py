import json
import os


class Config:
    def __init__(self, path=''):
        self.data = {}
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def get(self, key, default=None):
        return self.data.get(key, default)


class ConfigGame(Config):
    def __init__(self, path='data/config.json'):
        super().__init__(path)


class ConfigColor(Config):
    def __init__(self, path='data/colors.json'):
        super().__init__(path)