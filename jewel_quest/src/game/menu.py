import pygame
from src.common.config import ConfigGame
from src.common.screen import Screen


class ConfirmDialog(Screen):
    def __init__(self, config, message: str):
        super().__init__(config)
        dialog_width, dialog_height = 400, 200
        dx = self.width // 2 - dialog_width // 2
        dy = self.height // 2 - dialog_height // 2
        self.button_width, self.button_height = 150, 50
        self.message = message
        self.dialog_rect = pygame.Rect(dx, dy, dialog_width, dialog_height)
        self.yes_rect = pygame.Rect(dx + 60, dy + 120, self.button_width, self.button_height)
        self.no_rect = pygame.Rect(dx + 220, dy + 120, self.button_width, self.button_height)
        self.font = pygame.font.Font(None, 36)
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(150)
        self.overlay.fill((0, 0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.yes_rect.collidepoint(event.pos):
                return True
            if self.no_rect.collidepoint(event.pos):
                return False
        return None

    def draw(self, screen):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, self.colors["dark_purple"], self.dialog_rect, border_radius=12)
        pygame.draw.rect(screen, self.colors["light_purple"], self.dialog_rect, width=2, border_radius=12)
        text = self.font.render(self.message, True, self.colors["white"])
        text_rect = text.get_rect(center=(self.dialog_rect.centerx, self.dialog_rect.y + 60))
        screen.blit(text, text_rect)
        mouse_pos = pygame.mouse.get_pos()
        yes_color = self.colors["dark_blue"] if self.yes_rect.collidepoint(mouse_pos) else (60, 45, 100)
        pygame.draw.rect(screen, yes_color, self.yes_rect, border_radius=8)
        pygame.draw.rect(screen, self.colors["light_purple"], self.yes_rect, 2, border_radius=8)
        yes_text = self.font.render("Yes", True, self.colors["white"])
        screen.blit(yes_text, yes_text.get_rect(center=self.yes_rect.center))
        no_color = self.colors["dark_blue"] if self.no_rect.collidepoint(mouse_pos) else (60, 45, 100)
        pygame.draw.rect(screen, no_color, self.no_rect, border_radius=8)
        pygame.draw.rect(screen, self.colors["light_purple"], self.no_rect, 2, border_radius=8)
        no_text = self.font.render("No", True, self.colors["white"])
        screen.blit(no_text, no_text.get_rect(center=self.no_rect.center))


class Help(Screen):
    def __init__(self, config: ConfigGame):
        super().__init__(config)
        dialog_width, dialog_height = 400, 200
        self.reference_rect = pygame.Rect(self.width, self.height, dialog_width, dialog_height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return None

    def draw(self, screen):
        screen.fill(self.colors["black"])
        pygame.draw.rect(screen, self.colors["light_purple"], self.reference_rect, width=2, border_radius=12)
        title = self.font_title.render("JEWEL QUEST", True, self.colors["white"])
        lines = [
            "Swap adjacent stones,"
            "to match 3 or more.",
            "Mode 1: Score points before the time runs out.",
            "Mode 2: Complete levels by difficulty level.",
        ]
        hint = self.font_hint.render("Press ESC to return to menu", True, self.colors["gray"])
        screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 40)))
        for i, line in enumerate(lines):
            text = self.font_text.render(line, True, self.colors["light_gray"])
            screen.blit(text, text.get_rect(center=(self.width // 2, 180 + i * 50)))
        screen.blit(title, title.get_rect(center=(self.width // 2, 60)))


class Menu(Screen):
    def __init__(self, config: ConfigGame):
        super().__init__(config)
        items = [
            ("Start", "start"),
            ("Leaderboard", "records"),
            ("Help", "help"),
            ("Exit", "exit"),
        ]
        self.title = config.get("title")
        self.audio_config = config.get("audio")
        self.click_sound = pygame.mixer.Sound(self.audio_config["sound"])
        start_y = self.height // 2 - (len(items) * (self.button_height + 15)) // 2
        self.buttons = []
        for i, (text, action) in enumerate(items):
            x = self.width // 2 - self.button_width // 2
            y = start_y + i * (self.button_height + 15)
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.buttons.append((text, action, rect))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound = pygame.mixer.Sound(self.audio_config["sound"])
            click_sound.set_volume(self.audio_config["click_volume"])
            click_sound.play()
            for text, action, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    return action
        return None

    def draw(self, screen):
        screen.fill(self.colors["black"])
        title = self.font_title.render(self.title, True, self.colors["white"])
        title_rect = title.get_rect(center=(self.width // 2, self.height // 5))
        screen.blit(title, title_rect)
        mouse_pos = pygame.mouse.get_pos()
        for text, action, rect in self.buttons:
            color = self.colors["dark_blue"] if rect.collidepoint(mouse_pos) else self.colors["dark_purple"]
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, self.colors["light_purple"], rect, 2, border_radius=10)
            label = self.font_button.render(text, True, self.colors["white"])
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)


class ModeSelect(Screen):
    def __init__(self, config: ConfigGame):
        super().__init__(config)
        items = [
            ("Time", "time"),
            ("Score", "score"),
        ]
        start_y = self.height // 2 - (len(items) * (self.button_height + 15)) // 2
        self.buttons = []
        for i, (text, action) in enumerate(items):
            x = self.width // 2 - self.button_width // 2
            y = start_y + i * (self.button_height + 15)
            rectangle = pygame.Rect(x, y, self.button_width, self.button_height)
            self.buttons.append((text, action, rectangle))

    def draw(self, screen):
        screen.fill(self.colors["black"])
        title = self.font_title.render("Start", True, self.colors["white"])
        screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 5)))
        mouse_pos = pygame.mouse.get_pos()
        hint = self.font_hint.render("Press ESC to return to menu", True, self.colors["gray"])
        screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 40)))
        for text, action, rect in self.buttons:
            color = self.colors["dark_blue"] if rect.collidepoint(mouse_pos) else self.colors["dark_purple"]
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, self.colors["light_purple"], rect, 2, border_radius=10)
            label = self.font_button.render(text, True, self.colors["white"])
            screen.blit(label, label.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        if event.type == pygame.MOUSEBUTTONDOWN:
            for text, action, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    return action
        return None


class DifficultySelect(Screen):
    def __init__(self, config: ConfigGame):
        super().__init__(config)
        levels = config.get("levels")
        start_y = self.height // 2 - (len(levels) * (self.button_height + 15)) // 2
        self.buttons = []
        for i, level in enumerate(levels):
            x = self.width // 2 - self.button_width // 2
            y = start_y + i * (self.button_height + 15)
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.buttons.append((level["name"], level, rect))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, level, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    return level
        return None

    def draw(self, screen):
        screen.fill(self.colors["black"])
        title = self.font_title.render("Difficulty", True, self.colors["white"])
        screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 5)))
        mouse_pos = pygame.mouse.get_pos()
        for name, level, rect in self.buttons:
            color = self.colors["dark_blue"] if rect.collidepoint(mouse_pos) else self.colors["dark_purple"]
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, self.colors["light_purple"], rect, 2, border_radius=10)
            label = self.font_button.render(name, True, self.colors["white"])
            screen.blit(label, label.get_rect(center=rect.center))

