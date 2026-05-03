import pygame
from src.game.config import Config


class ConfirmDialog:
    def __init__(self, config, message: str):
        self.message = message
        self.screen_config = config.get("screen")
        self.width = self.screen_config["width"]
        self.height = self.screen_config["height"]
        dw, dh = 400, 200
        dx = self.width // 2 - dw // 2
        dy = self.height // 2 - dh // 2
        self.dialog_rect = pygame.Rect(dx, dy, dw, dh)
        button_width, button_height = 150, 50
        self.yes_rect = pygame.Rect(dx + 60, dy + 120, button_width, button_height)
        self.no_rect = pygame.Rect(dx + 220, dy + 120, button_width, button_height)
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
        pygame.draw.rect(screen, (50, 40, 90), self.dialog_rect, border_radius=12)
        pygame.draw.rect(screen, (150, 120, 200), self.dialog_rect, width=2, border_radius=12)
        text = self.font.render(self.message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.dialog_rect.centerx, self.dialog_rect.y + 60))
        screen.blit(text, text_rect)

        mouse_pos = pygame.mouse.get_pos()

        yes_color = (80, 60, 120) if self.yes_rect.collidepoint(mouse_pos) else (60, 45, 100)
        pygame.draw.rect(screen, yes_color, self.yes_rect, border_radius=8)
        pygame.draw.rect(screen, (150, 120, 200), self.yes_rect, 2, border_radius=8)
        yes_text = self.font.render("Да", True, (255, 255, 255))
        screen.blit(yes_text, yes_text.get_rect(center=self.yes_rect.center))

        no_color = (80, 60, 120) if self.no_rect.collidepoint(mouse_pos) else (60, 45, 100)
        pygame.draw.rect(screen, no_color, self.no_rect, border_radius=8)
        pygame.draw.rect(screen, (150, 120, 200), self.no_rect, 2, border_radius=8)
        no_text = self.font.render("Нет", True, (255, 255, 255))
        screen.blit(no_text, no_text.get_rect(center=self.no_rect.center))


class Reference:
    def __init__(self, config: Config):
        screen_config = config.get("screen")
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        dw, dh = 400, 200
        self.reference_rect = pygame.Rect(self.width, self.height, dw, dh)
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 50)
        self.font_hint = pygame.font.Font(None, 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return None

    def draw(self, screen):
        screen.fill((30, 20, 50))
        pygame.draw.rect(screen, (150, 120, 200), self.reference_rect, width=2, border_radius=12)
        title = self.font_title.render("JEWEL QUEST", True, (255, 255, 255))
        lines = [
            "Меняйте местами соседние камни",
            "чтобы собрать 3 и более в ряд.",
            "Режим 1: успей набрать очки за время.",
            "Режим 2: пройди уровни по целям.",
        ]
        hint = self.font_hint.render("Нажмите ESC для выхода в меню", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 40)))
        for i, line in enumerate(lines):
            text = self.font_text.render(line, True, (200, 200, 200))
            screen.blit(text, text.get_rect(center=(self.width // 2, 180 + i * 50)))
        screen.blit(title, title.get_rect(center=(self.width // 2, 60)))


class Menu:
    def __init__(self, config: Config):
        self.config = config
        screen_config = config.get("screen")
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        self.title = config.get("title")
        self.audio_config = config.get("audio")
        self.click_sound = pygame.mixer.Sound(self.audio_config["sound"])
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 42)
        items = [
            ("Начать игру", "start"),
            ("Таблица рекордов", "records"),
            ("Справка", "help"),
            ("Выход", "exit"),
        ]
        button_w, button_h = 300, 55
        start_y = self.height // 2 - (len(items) * (button_h + 15)) // 2
        self.buttons = []
        for i, (text, action) in enumerate(items):
            x = self.width // 2 - button_w // 2
            y = start_y + i * (button_h + 15)
            rect = pygame.Rect(x, y, button_w, button_h)
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
        screen.fill((30, 20, 50))
        title = self.font_title.render(self.title, True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 5))
        screen.blit(title, title_rect)
        mouse_pos = pygame.mouse.get_pos()
        for text, action, rect in self.buttons:
            color = (80, 60, 120) if rect.collidepoint(mouse_pos) else (50, 40, 90)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (150, 120, 200), rect, 2, border_radius=10)

            label = self.font_button.render(text, True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)


class ModeSelect:
    def __init__(self, config: Config):
        screen_config = config.get("screen")
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        self.font_title = pygame.font.Font(None, 62)
        self.font_text = pygame.font.Font(None, 40)
        self.font_button = pygame.font.Font(None, 42)
        items = [
            ("На время", "time"),
            ("По очкам", "score"),
        ]
        button_width, button_height = 300, 50
        start_y = self.height // 2 - (len(items) * (button_height + 15)) // 2
        self.buttons = []
        for i, (text, action) in enumerate(items):
            x = self.width // 2 - button_width // 2
            y = start_y + i * (button_height + 15)
            rectangle = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append((text, action, rectangle))

    def draw(self, screen):
        screen.fill((30, 20, 50))
        title = self.font_title.render("Начать игру", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 5)))
        mouse_pos = pygame.mouse.get_pos()
        hint = self.font_text.render("Нажмите ESC для выхода в меню", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 40)))
        for text, action, rect in self.buttons:
            color = (80, 60, 120) if rect.collidepoint(mouse_pos) else (50, 40, 90)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (150, 120, 200), rect, 2, border_radius=10)
            label = self.font_button.render(text, True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        if event.type == pygame.MOUSEBUTTONDOWN:
            for text, action, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    return action
        return None


class DifficultySelect:
    def __init__(self, config):
        screen_config = config.get("screen")
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        self.font_title = pygame.font.Font(None, 62)
        self.font_button = pygame.font.Font(None, 42)
        levels = config.get("levels")
        button_w, button_h = 300, 55
        start_y = self.height // 2 - (len(levels) * (button_h + 15)) // 2
        self.buttons = []
        for i, level in enumerate(levels):
            x = self.width // 2 - button_w // 2
            y = start_y + i * (button_h + 15)
            rect = pygame.Rect(x, y, button_w, button_h)
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
        screen.fill((30, 20, 50))
        title = self.font_title.render("Выберите сложность", True, (255, 220, 80))
        screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 5)))
        mouse_pos = pygame.mouse.get_pos()
        for name, level, rect in self.buttons:
            color = (80, 60, 120) if rect.collidepoint(mouse_pos) else (50, 40, 90)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (150, 120, 200), rect, 2, border_radius=10)
            label = self.font_button.render(name, True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=rect.center))

