import pygame

from src.game.board import Board
from src.game.leaderboard import LeaderBoard


class Game:
    def __init__(self, config, mode, level=None):
        board_config = config.get("board")
        game_config = config.get("game")
        screen_config = config.get("screen")
        self.mode = mode
        self.score = 0
        self.selected = None
        self.time_left = game_config["time_limit"]
        self.last_tick = pygame.time.get_ticks()
        if mode == "score" and level is not None:
            self.goal = level["goal"]
            self.moves_left = level["moves"]
        else:
            self.goal = None
            self.moves_left = None
        self.board = Board(row=board_config["rows"], column=board_config["columns"])
        self.board.fill()
        self.cell_size = board_config["cell_size"]
        board_pixel_w = board_config["columns"] * board_config["cell_size"]
        board_pixel_h = board_config["rows"] * board_config["cell_size"]
        self.points_per_jewel = game_config["points_per_jewel"]
        self.offset_x = (screen_config["width"] - board_pixel_w) // 2
        self.offset_y = (screen_config["height"] - board_pixel_h) // 2

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
        if self.mode == "score":
            moves_label = font_label.render("Ходов", True, (255, 255, 255))
            screen.blit(moves_label, (panel_x, panel_y + 110))
            moves_value = font_value.render(str(self.moves_left), True, (255, 255, 255))
            screen.blit(moves_value, (panel_x, panel_y + 145))
            goal_label = font_label.render("Цель", True, (255, 255, 255))
            screen.blit(goal_label, (panel_x, panel_y + 220))
            goal_value = font_value.render(str(self.goal), True, (255, 220, 80))
            screen.blit(goal_value, (panel_x, panel_y + 255))

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
                    if self.mode == "score":
                        self.moves_left -= 1
                self.selected = None

    def is_over(self):
        if self.mode == "time":
            return self.time_left <= 0
        if self.mode == "score":
            return self.moves_left <= 0


class GameOver:
    def __init__(self, config, score, mode, leaderboard):
        self.score = score
        self.mode = mode
        self.leaderboard = leaderboard
        self.is_record = leaderboard.is_high_score(score)
        self.name_input = ""
        self.input_activate = True
        screen_config = config.get("screen")
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 42)
        button_width, button_height = 220, 55
        self.menu_rect = pygame.Rect(self.width // 2 - button_width - 20, self.height - 120, button_width, button_height)
        self.retry_rect = pygame.Rect(self.width // 2 + 20, self.height - 120, button_width, button_height)

    def handle_event(self, event, leaderboard: LeaderBoard):
        if self.is_record and self.input_activate:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    leaderboard.add(self.name_input, self.score, self.mode)
                    self.input_activate = False
                elif event.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                else:
                    self.name_input += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(event.pos): return "menu"
            if self.retry_rect.collidepoint(event.pos): return "retry"
            return None

    def draw(self, screen):
        screen.fill((20, 15, 40))
        title = self.font_title.render("Игра окончена", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(self.width // 2, 100)))
        score_text = self.font_text.render(f"Ваш счет: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, score_text.get_rect(center=(self.width // 2, 200)))
        if self.is_record:
            record_text = self.font_text.render("Новый рекорд", True, (255, 255, 255))
            screen.blit(record_text, record_text.get_rect(center=(self.width // 2, 280)))
            if self.input_activate:
                prompt = self.font_text.render("Введите имя: ", True, (200, 200, 200))
                screen.blit(prompt, prompt.get_rect(center=(self.width // 2, 350)))
                input_rect = pygame.Rect(self.width // 2 - 150, 390, 300, 50)
                pygame.draw.rect(screen, (50, 40, 90), input_rect, border_radius=8)
                pygame.draw.rect(screen, (150, 120, 200), input_rect, 2, border_radius=8)
                name_text = self.font_text.render(self.name_input, True, (255, 255, 255))
                screen.blit(name_text, name_text.get_rect(center=input_rect.center))
                hint = self.font_button.render("Нажмите Enter для сохранения", True, (150, 150, 150))
                screen.blit(hint, hint.get_rect(center=(self.width // 2, 460)))
            else:
                saved = self.font_text.render("Рекорд сохранен", True, (100, 255, 100))
                screen.blit(saved, saved.get_rect(center=(self.width // 2, 370)))
        mouse_pos = pygame.mouse.get_pos()
        for rect, label in [(self.menu_rect, "В меню"), (self.retry_rect, "Играть снова")]:
            color = (80, 60, 120) if rect.collidepoint(mouse_pos) else (50, 40, 90)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (150, 120, 200), rect, 2, border_radius=8)
            text = self.font_button.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))