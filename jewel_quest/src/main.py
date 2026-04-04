import pygame
import sys

FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jewel Quest")
    timer = pygame.time.Clock()

    while True:
        timer.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((70, 130, 180))
        pygame.display.flip()


if __name__ == "__main__":
    main()