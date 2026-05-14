import pygame
from src.common.config import ConfigGame
from src.game.menu import Menu, ConfirmDialog, Help, ModeSelect, DifficultySelect
from src.game.leaderboard import LeaderBoardScreen, LeaderBoard
from src.game.game import Game, GameOver


class App:
    def __init__(self):
        self.config = ConfigGame()
        self.audio_config = self.config.get("audio")
        self.screen_config = self.config.get("screen")
        pygame.init()
        pygame.key.set_repeat(400, 50)
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.screen_config["width"], self.screen_config["height"]))
        pygame.display.set_caption(self.config.get("title"))
        self.clock = pygame.time.Clock()
        self._play_music("menu_music")
        self.lead = LeaderBoard()
        self.menu = Menu(self.config)
        self.ref = Help(self.config)
        self.dialog = ConfirmDialog(self.config, "Quit?")
        self.mode_select = ModeSelect(self.config)
        self.difficulty_select = DifficultySelect(self.config)
        self.leaderboard = LeaderBoardScreen(self.config, self.lead)
        self.state = "menu"
        self.overlay = None
        self.game = None
        self.game_over = None
        self.current_level = None
        self.running = True

    def _play_music(self, key):
        pygame.mixer.music.load(self.audio_config[key])
        pygame.mixer.music.set_volume(self.audio_config["music_volume"])
        pygame.mixer.music.play(-1)

    def _set_overlay(self, name):
        self.overlay = name

    def _clear_overlay(self):
        self.overlay = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self._handle_event(event)
            self._draw()
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(self.screen_config["fps"])
        pygame.quit()

    def _handle_event(self, event):
        match self.overlay:
            case "quit":
                result = self.dialog.handle_event(event)
                if result is True:
                    self.running = False
                elif result is False:
                    self._clear_overlay()
            case "help":
                if self.ref.handle_event(event):
                    self._clear_overlay()
            case "leaderboard":
                if self.leaderboard.handle_event(event):
                    self._clear_overlay()
            case "mode":
                result = self.mode_select.handle_event(event)
                match result:
                    case "back":
                        self._clear_overlay()
                    case "time":
                        self._start_game("time")
                    case "score":
                        self._set_overlay("difficulty")
            case "difficulty":
                result = self.difficulty_select.handle_event(event)
                if result == "back":
                    self._set_overlay("mode")
                elif result is not None:
                    self.current_level = result
                    self._start_game("score", result)
            case None:
                if self.state == "menu":
                    self._handle_menu(event)
                elif self.state == "game":
                    self.game.handle_event(event)
                elif self.state == "game_over":
                    self._handle_game_over(event)

    def _handle_menu(self, event):
        match self.menu.handle_event(event):
            case "exit":
                self._set_overlay("quit")
            case "start":
                self._set_overlay("mode")
            case "help":
                self._set_overlay("help")
            case "records":
                self._set_overlay("leaderboard")

    def _handle_game_over(self, event):
        result = self.game_over.handle_event_with_leaderboard(event, self.lead)
        if result == "menu":
            self.state = "menu"
            self.game_over = None
            self._play_music("menu_music")
        elif result == "retry":
            self._start_game(self.game.mode, self.current_level)

    def _start_game(self, mode, level=None):
        self.game = Game(self.config, mode, level)
        self.state = "game"
        self.game_over = None
        self._clear_overlay()
        self._play_music("level_music")

    def _draw(self):
        match self.overlay:
            case "quit":
                self.menu.draw(self.screen)
                self.dialog.draw(self.screen)
            case "help":
                self.ref.draw(self.screen)
            case "leaderboard":
                self.leaderboard.draw(self.screen)
            case "mode":
                self.mode_select.draw(self.screen)
            case "difficulty":
                self.difficulty_select.draw(self.screen)
            case None:
                if self.state == "game":
                    if self.game is None:
                        return
                    self.game.update()
                    if self.game.is_over():
                        self.state = "game_over"
                        self.game_over = GameOver(
                            self.config, self.game.score,
                            self.game.mode, self.lead, self.game.goal
                        )
                    self.game.draw(self.screen)
                elif self.state == "game_over":
                    self.game_over.draw(self.screen)
                else:
                    self.menu.draw(self.screen)