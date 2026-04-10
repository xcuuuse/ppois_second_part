import pygame
import sys

from src.common.board import Board
from src.renderer.renderer import Renderer
FPS = 30
CELL_SIZE = 64


def main():
    board = Board(5, 5)
    board.fill()
    clock = pygame.time.Clock()
    renderer = Renderer(board)
    selected = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                column = x // CELL_SIZE
                row = y // CELL_SIZE
                if selected is None:
                    selected = (row, column)
                else:
                    board.swap(selected[0], selected[1], row, column)
                    selected = None
            if event.type == pygame.K_ESCAPE:
                selected = None
        renderer.draw(selected)
        clock.tick(FPS)


if __name__ == "__main__":
    main()