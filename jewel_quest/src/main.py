import pygame
import sys
from common.board import Board
FPS = 30


def main():
    """pygame.init()
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
        pygame.display.flip()"""
    board = Board(5, 4)
    board.fill()
    board.print_board()
    row, column = int(input()), int(input())
    swap, swap1 = int(input()), int(input())
    board.swap(row, column, swap, swap1)
    board.print_board()


if __name__ == "__main__":
    main()