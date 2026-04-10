import pygame
from src.common.board import Board
CELL_SIZE = 64
COLORS = {
    "R": (220, 50, 50),
    "G": (55, 235, 52),
    "B": (52, 177, 235),
    "Y": (235, 226, 52),
    "P": (204, 52, 235),
    None: (30, 30, 30)
}


class Renderer:
    def __init__(self, board: Board):
        self.board = board
        self.screen = pygame.display.set_mode((
            board.column * CELL_SIZE,
            board.row * CELL_SIZE
        ))
        pygame.display.set_caption("Jewel Quest")

    def draw(self, selected=None):
        self.screen.fill((0, 0, 0))
        for row in range(self.board.row):
            for column in range(self.board.column):
                color = COLORS[self.board.field[row][column]]
                rectangle = (column * CELL_SIZE + 2, row * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                pygame.draw.rect(self.screen, color, rectangle)
                if selected == (row, column):
                    pygame.draw.rect(self.screen, (255, 255, 255), rectangle, width=3, border_radius=8)
        pygame.display.flip()

