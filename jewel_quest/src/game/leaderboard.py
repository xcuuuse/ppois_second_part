import os
import json
import pygame
from src.common.config import ConfigGame
from src.common.screen import Screen


class LeaderBoard:
    def __init__(self, path='data/leaderboard.json', max_records=5):
        self.max_records = max_records
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
        self.records = self.records[:self.max_records]
        self._save()

    def is_high_score(self, score):
        if score <= 0:
            return False
        if len(self.records) == 0:
            return True
        return score > self.records[0]["score"]


class LeaderBoardScreen(Screen):
    def __init__(self, config: ConfigGame, leaderboard: LeaderBoard):
        super().__init__(config)
        self.leaderboard = leaderboard
        dw, dh = 400, 200
        self.leaderboard_rect = pygame.Rect(self.width, self.height, dw, dh)
        self.font_text = pygame.font.Font(None, 60)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return None

    def draw(self, screen):
        screen.fill(self.colors["black"])
        title = self.font_title.render("Leaderboard", True, self.colors["white"])
        screen.blit(title, title.get_rect(center=(self.width // 2, 60)))
        if self.leaderboard is None or len(self.leaderboard.records) == 0:
            empty = self.font_text.render("No records yet", True, self.colors["gray"])
            screen.blit(empty, empty.get_rect(center=(self.width // 2, self.height // 2)))
        else:
            for i, record in enumerate(self.leaderboard.records):
                line = f"{i + 1}.  {record['name']}  —  {record['score']}"
                text = self.font_text.render(line, True, self.colors["white"])
                screen.blit(text, text.get_rect(center=(self.width // 2, 150 + i * 55)))
        hint = self.font_hint.render("Press ESC to return to menu", True, self.colors["gray"])
        screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 40)))