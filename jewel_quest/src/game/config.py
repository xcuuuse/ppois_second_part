import json
import os


class Config:
    def __init__(self, path='data/config.json'):
        self.data = {}
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def get(self, key, default=None):
        return self.data.get(key, default)

