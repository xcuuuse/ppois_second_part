import os
import json
from src.game.config import Config
import pygame


class LeaderBoard:
    def __init__(self, path='data/leaderboard.json'):
        self.path = path
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.records = data.get("records", [])

    def _save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump({"records": self.records}, f, ensure_ascii=False, indent=2)

    def add(self, name, score, mode):
        self.records.append({"name": name, "score": score, "mode": mode})
        self.records.sort(key=lambda x: x["score"], reverse=True)
        self.records = self.records[:10]
        self._save()

    def is_high_score(self, score):
        if len(self.records) < 10:
            return True
        return score > self.records[-1]["score"]


class LeaderBoardScreen:
    def __init__(self, config: Config, leaderboard: LeaderBoard):
        self.leaderboard = leaderboard
        screen_config = config.get("screen")
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        dw, dh = 400, 200
        self.leaderboard_rect = pygame.Rect(self.width, self.height, dw, dh)
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 60)
        self.font_hint = pygame.font.Font(None, 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return None

    def draw(self, screen):
        screen.fill((30, 20, 50))
        title = self.font_title.render("Таблица рекордов", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(self.width // 2, 60)))
        if self.leaderboard is None or len(self.leaderboard.records) == 0:
            empty = self.font_text.render("Рекордов пока нет", True, (150, 150, 150))
            screen.blit(empty, empty.get_rect(center=(self.width // 2, self.height // 2)))
        else:
            for i, record in enumerate(self.leaderboard.records):
                line = f"{i + 1}.  {record['name']}  —  {record['score']}"
                text = self.font_text.render(line, True, (255, 255, 255))
                screen.blit(text, text.get_rect(center=(self.width // 2, 150 + i * 55)))
        hint = self.font_hint.render("Нажмите ESC для выхода в меню", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 40)))