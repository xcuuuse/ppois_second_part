import pygame
from src.common.config import ConfigGame, ConfigColor


class Screen:
    def __init__(self, config: ConfigGame):
        screen_config = config.get("screen")
        config_color = ConfigColor()
        colors_raw = config_color.get("colors")
        self.colors = {key: tuple(value) for key, value in colors_raw.items()}
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        self.button_width = screen_config["button_width"]
        self.button_height = screen_config["button_height"]
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 42)
        self.font_hint = pygame.font.Font(None, 36)

    def handle_event(self, event):
        return None

    def draw(self, screen):
        pass

