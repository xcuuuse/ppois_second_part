import pygame
from src.game.config import Config
from src.game.menu import Menu, ConfirmDialog, Reference, ModeSelect, DifficultySelect
from src.game.leaderboard import LeaderBoardScreen, LeaderBoard
from src.game.game import Game, GameOver


def main():
    pygame.init()
    config = Config()
    game = None
    audio_config = config.get("audio")
    pygame.mixer.init()
    pygame.mixer.music.load(audio_config["menu_music"])
    pygame.mixer.music.set_volume(audio_config["music_volume"])
    pygame.mixer.music.play(-1)
    dialog = ConfirmDialog(config, "Хотите выйти из игры?")
    screen_config = config.get("screen")
    screen = pygame.display.set_mode((screen_config["width"], screen_config["height"]))
    pygame.display.set_caption(config.get("title"))
    clock = pygame.time.Clock()
    menu = Menu(config)
    ref = Reference(config)
    difficulty_select = DifficultySelect(config)
    show_difficulty = False
    selected_level = None
    leaderboard = LeaderBoard()
    state = "menu"
    show_dialog = False
    show_help = False
    game_over = None
    show_leaderboard = False
    running = True
    lead = LeaderBoardScreen(config, leaderboard)
    mode_select = ModeSelect(config)
    show_mode_select = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "menu" and not (
                show_mode_select or
                show_leaderboard or
                show_help or
                show_dialog
            ):
                action = menu.handle_event(event)
                if action == "exit":
                    show_dialog = True
                if action == "start":
                    show_mode_select = True
                if action == "help":
                    show_help = True
                if action == "records":
                    show_leaderboard = True
            if show_difficulty:
                result = difficulty_select.handle_event(event)
                if result == "back":
                    show_difficulty = False
                    show_mode_select = True
                elif result is not None:
                    game = Game(config, "score", result)  # передаём выбранный уровень
                    state = "game"
                    show_difficulty = False
            elif show_mode_select:
                result = mode_select.handle_event(event)
                if result == "back":
                    show_mode_select = False
                elif result == "time":
                    game = Game(config, "time")
                    state = "game"
                    show_mode_select = False
                elif result == "score":
                    show_mode_select = False
                    show_difficulty = True
            elif show_dialog:
                result = dialog.handle_event(event)
                if result == True:
                    running = False
                elif result == False:
                    show_dialog = False
            elif show_help:
                result = ref.handle_event(event)
                if result == True:
                    show_help = False
            elif show_leaderboard:
                result = lead.handle_event(event)
                if result == True:
                    show_leaderboard = False
            elif state == "game":
                game.handle_event(event)
            elif state == "game_over":
                result = game_over.handle_event(event, leaderboard)
                if result == "menu":
                    state = "menu"
                    game_over = None
                elif result == "retry":
                    game = Game(config, game.mode)
                    state = "game"
                    game_over = None
        if show_difficulty:
            difficulty_select.draw(screen)
        elif show_mode_select:
            mode_select.draw(screen)
        elif show_dialog:
            dialog.draw(screen)
        elif show_help:
            ref.draw(screen)
        elif show_leaderboard:
            lead.draw(screen)
        elif state == "game":
            game.update()
            if game.is_over():
                state = "game_over"
                game_over = GameOver(config, game.score, game.mode, leaderboard)
            game.draw(screen)
        elif state == "game_over":
            game_over.draw(screen)
        else:
            menu.draw(screen)
        pygame.display.flip()
        clock.tick(screen_config["fps"])

    pygame.quit()


if __name__ == "__main__":
    main()

