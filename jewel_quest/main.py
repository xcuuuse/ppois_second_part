import pygame
from src.game.config import Config
from src.game.menu import Menu, ConfirmDialog, Reference, ModeSelect
from src.game.leaderboard import LeaderBoardScreen, LeaderBoard
from src.game.game import Game


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
    leaderboard = LeaderBoard()
    state = "menu"
    show_dialog = False
    show_help = False
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
            if show_mode_select:
                result = mode_select.handle_event(event)
                if result == "back":
                    show_mode_select = False
                elif result == "time":
                    game = Game(config, "time")
                    state = "game"
                    show_mode_select = False
                elif result == "score":
                    game = Game(config, "score")
                    state = "game"
                    show_mode_select = False
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
        if state == "menu":
            menu.draw(screen)
        if show_mode_select:
            mode_select.draw(screen)
        elif show_dialog:
            dialog.draw(screen)
        elif show_help:
            ref.draw(screen)
        elif show_leaderboard:
            lead.draw(screen)
        elif state == "game":
            game.draw(screen)
        else:
            menu.draw(screen)



        pygame.display.flip()
        clock.tick(screen_config["fps"])

    pygame.quit()


if __name__ == "__main__":
    main()

