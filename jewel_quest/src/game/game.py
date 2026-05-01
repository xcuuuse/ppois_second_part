import pygame

from src.game.board import Board

class Game:
    def __init__(self, config, mode):
        board_config = config.get("board")
        self.board = Board(row=board_config["rows"], column=board_config["columns"])
        self.board.fill()
        self.cell_size = board_config["cell_size"]
        self.offset_x = board_config["offset_x"]
        self.offset_y = board_config["offset_y"]
        self.mode = mode
        self.score = 0
        self.selected = None

    def draw(self, screen):
        screen.fill((20, 15, 40))
        for i in range(self.board.row):
            for j in range(self.board.column):
                x = self.offset_x + j * self.cell_size
                y = self.offset_y + i * self.cell_size
                jewel = self.board.field[i][j]
                if not jewel:
                    continue
                color = jewel.value
                padding = 6
                rect = pygame.Rect(x + padding, y + padding, self.cell_size - padding * 2, self.cell_size - padding * 2)
                pygame.draw.rect(screen, color, rect, border_radius=8)
                if self.selected == (i, j):
                    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=8)

    def get_cell(self, mouse_x, mouse_y):
        col = (mouse_x - self.offset_x) // self.cell_size
        row = (mouse_y - self.offset_y) // self.cell_size
        if 0 <= row < self.board.row and 0 <= col < self.board.column:
            return (row, col)
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = self.get_cell(*event.pos)
            if cell is None:
                self.selected = None
                return
            if self.selected is None:
                self.selected = cell
            else:
                self.board.swap(*self.selected, *cell)
                self.selected = None

