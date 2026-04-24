import json
import os


class Config:
    def __init__(self, path='data/config.json'):
        self.data = {}
        base_dir = os.path.dirname(os.path.abspath(__file__))  # папка где лежит config.py
        full_path = os.path.join(base_dir, '..', path)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def get(self, key, default=None):
        return self.data.get(key, default)

