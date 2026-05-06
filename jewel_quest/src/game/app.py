import pygame
from src.common.config import ConfigGame
from src.game.menu import Menu, ConfirmDialog, Reference, ModeSelect, DifficultySelect
from src.game.leaderboard import LeaderBoardScreen, LeaderBoard
from src.game.game import Game, GameOver


class App:
    def __init__(self):
        self.config = ConfigGame()
        self.game = None
        self.game_over = None
        self.audio_config = self.config.get("audio")
        pygame.init()
        pygame.key.set_repeat(400, 50)
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load(self.audio_config["menu_music"])
        pygame.mixer.music.set_volume(self.audio_config["music_volume"])
        pygame.mixer.music.play(-1)
        pygame.display.set_caption(self.config.get("title"))
        self.dialog = ConfirmDialog(self.config, "Quit?")
        self.screen_config = self.config.get("screen")
        self.screen = pygame.display.set_mode((self.screen_config["width"], self.screen_config["height"]))
        self.menu = Menu(self.config)
        self.ref = Reference(self.config)
        self.difficulty_select = DifficultySelect(self.config)
        self.mode_select = ModeSelect(self.config)
        self.lead = LeaderBoard()
        self.leaderboard = LeaderBoardScreen(self.config, self.lead)
        self.state = "menu"
        self.show_mode_select = self.show_difficulty = self.show_leaderboard = self.show_help = self.show_quit = False
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.state == "menu" and not (
                    self.show_mode_select or
                    self.show_leaderboard or
                    self.show_help or
                    self.show_quit
                ):
                    self._menu(event)
                if self.show_difficulty:
                    self._show_difficulty(event)
                elif self.show_mode_select:
                    self._show_mode_select(event)
                elif self.show_quit:
                    self._show_quit(event)
                elif self.show_help:
                    self._show_help(event)
                elif self.show_leaderboard:
                    self._show_leaderboard(event)
                elif self.state == "game":
                    self.game.handle_event(event)
                elif self.state == "game_over":
                    self._game_over(event, leaderboard=self.lead)
            if self.show_difficulty:
                self.difficulty_select.draw(self.screen)
            elif self.show_mode_select:
                self.mode_select.draw(self.screen)
            elif self.show_quit:
                self.dialog.draw(self.screen)
            elif self.show_help:
                self.ref.draw(self.screen)
            elif self.show_leaderboard:
                self.leaderboard.draw(self.screen)
            elif self.state == "game":
                self.game.update()
                if self.game.is_over():
                    self.state = "game_over"
                    self.game_over = GameOver(self.config, self.game.score, self.game.mode, self.lead)
                self.game.draw(self.screen)
            elif self.state == "game_over":
                self.game_over.draw(self.screen)
            else:
                self.menu.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.screen_config["fps"])
        pygame.quit()

    def _menu(self, event):
        action = self.menu.handle_event(event)
        if action == "exit":
            self.show_quit = True
        elif action == "start":
            self.show_mode_select = True
        elif action == "help":
            self.show_help = True
        elif action == "records":
            self.show_leaderboard = True

    def _show_difficulty(self, event):
        result = self.difficulty_select.handle_event(event)
        self.current_level = result
        self.game = Game(self.config, "score", result)
        if result == "back":
            self.show_mode_select = True
            self.show_difficulty = False
        elif result is not None:
            self.game = Game(self.config, "score", result)
            self.state = "game"
            self.show_difficulty = False

    def _show_mode_select(self, event):
        result = self.mode_select.handle_event(event)
        match result:
            case "back":
                self.show_mode_select = False
            case "time":
                self.game = Game(self.config, mode="time")
                self.state = "game"
                self.show_mode_select = False
                pygame.mixer.music.load(self.audio_config["level_music"])
                pygame.mixer.music.play(-1)
            case "score":
                self.show_mode_select = False
                self.show_difficulty = True
                pygame.mixer.music.load(self.audio_config["level_music"])
                pygame.mixer.music.play(-1)

    def _show_quit(self, event):
        result = self.dialog.handle_event(event)
        if result == True:
            self.running = False
        elif result == False:
            self.show_quit = False

    def _show_help(self, event):
        result = self.ref.handle_event(event)
        if result == True:
            self.show_help = False

    def _show_leaderboard(self, event):
        result = self.leaderboard.handle_event(event)
        if result == True:
            self.show_leaderboard = False

    def _game_over(self, event, leaderboard):
        result = self.game_over.handle_event_with_leaderboard(event, leaderboard)
        if result == "menu":
            self.state = "menu"
            self.game_over = None
            pygame.mixer.music.load(self.audio_config["level_music"])
            pygame.mixer.music.play(-1)
        if result == "retry":
            if self.game.mode == "score":
                self.game = Game(self.config, "score", self.current_level)
            else:
                self.game = Game(self.config, "time")
            self.state = "game"
            self.game_over = None
            pygame.mixer.music.load(self.audio_config["level_music"])
            pygame.mixer.music.play(-1)







