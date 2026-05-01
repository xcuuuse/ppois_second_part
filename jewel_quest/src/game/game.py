import pygame

from src.game.board import Board


class Game:
    def __init__(self, config, mode):
        board_config = config.get("board")
        game_config = config.get("game")
        self.time_left = game_config["time_limit"]
        self.last_tick = pygame.time.get_ticks()
        screen_config = config.get("screen")
        self.board = Board(row=board_config["rows"], column=board_config["columns"])
        self.board.fill()
        self.cell_size = board_config["cell_size"]
        board_pixel_w = board_config["columns"] * board_config["cell_size"]
        board_pixel_h = board_config["rows"] * board_config["cell_size"]
        self.points_per_jewel = game_config["points_per_jewel"]
        self.offset_x = (screen_config["width"] - board_pixel_w) // 2
        self.offset_y = (screen_config["height"] - board_pixel_h) // 2
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
        panel_x = self.offset_x + self.board.column * self.cell_size + 30
        panel_y = self.offset_y
        font_label = pygame.font.Font(None, 46)
        font_value = pygame.font.Font(None, 56)
        label = font_label.render("Очки", True, (255, 255, 255))
        screen.blit(label, (panel_x, panel_y))
        value = font_value.render(str(self.score), True, (255, 255, 255))
        screen.blit(value, (panel_x, panel_y + 35))
        if self.mode == "time":
            time_label = font_label.render("Время", True, (255, 255, 255))
            screen.blit(time_label, (panel_x, panel_y + 110))
            seconds = max(0, int(self.time_left))
            time_str = f"{seconds // 60}:{seconds % 60:02d}"
            time_value = font_value.render(time_str, True, (255, 255, 255))
            screen.blit(time_value, (panel_x, panel_y + 145))

    def update(self):
        if self.mode == "time":
            now = pygame.time.get_ticks()
            self.time_left -= (now - self.last_tick) / 1000
            self.last_tick = now

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
                removed = self.board.swap(*self.selected, *cell)
                if removed:
                    self.score += removed * self.points_per_jewel
                self.selected = None


