import pygame
from src.game.config import Config
from src.game.menu import Menu, ConfirmDialog, Reference


def main():
    pygame.init()
    config = Config()
    dialog = ConfirmDialog(config, "Хотите выйти из игры?")
    screen_config = config.get("screen")
    screen = pygame.display.set_mode((screen_config["width"], screen_config["height"]))
    pygame.display.set_caption(config.get("title"))
    clock = pygame.time.Clock()
    menu = Menu(config)
    ref = Reference(config)
    state = "menu"
    show_dialog = False
    show_help = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "menu" and not show_dialog and not show_help:
                action = menu.handle_event(event)
                if action == "exit":
                    show_dialog = True
                if action == "start":
                    print("x")
                if action == "help":
                    show_help = True
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
        if state == "menu":
            menu.draw(screen)
        if show_dialog:
            dialog.draw(screen)
        if show_help:
            ref.draw(screen)
        pygame.display.flip()
        clock.tick(screen_config["fps"])

    pygame.quit()


if __name__ == "__main__":
    main()

