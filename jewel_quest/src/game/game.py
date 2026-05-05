import pygame
from src.game.board import Board
from src.game.leaderboard import LeaderBoard
from src.common.config import ConfigGame, ConfigColor
from src.common.jewel import JEWEL
from src.common.screen import Screen


class Game(Screen):
    def __init__(self, config: ConfigGame, mode, level=None):
        screen_config = config.get("screen")
        anim_config = config.get("animation")
        super().__init__(config)
        board_config = config.get("board")
        game_config = config.get("game")
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
        self.anim_state = "idle"
        self.anim_start = 0
        self.swap_from = None
        self.swap_to = None
        self.anim_duration = anim_config["anim_duration"]
        self.removing = set()
        self.pending_special = None
        self.remove_start = 0
        self.remove_duration = anim_config["remove_duration"]
        self.drop_offsets = {}
        self.drop_start = 0
        self.drop_duration = anim_config["drop_duration"]

    def draw(self, screen):
        screen.fill((20, 15, 40))
        now = pygame.time.get_ticks()
        progress = min(1.0, (now - self.anim_start) / self.anim_duration) if self.anim_state == "swapping" else 1.0
        for i in range(self.board.row):
            for j in range(self.board.column):
                x = self.offset_x + j * self.cell_size
                y = self.offset_y + i * self.cell_size
                jewel = self.board.field[i][j]
                if not jewel:
                    continue
                dx, dy = 0, 0
                if self.anim_state == "swapping":
                    r1, c1 = self.swap_from
                    r2, c2 = self.swap_to
                    if (i, j) == (r1, c1):
                        dx = (c2 - c1) * self.cell_size * progress
                        dy = (r2 - r1) * self.cell_size * progress
                    elif (i, j) == (r2, c2):
                        dx = (c1 - c2) * self.cell_size * progress
                        dy = (r1 - r2) * self.cell_size * progress
                if self.anim_state == "dropping" and (i, j) in self.drop_offsets:
                    drop_progress = min(1.0, (now - self.drop_start) / self.drop_duration)
                    cells = self.drop_offsets[(i, j)]
                    dy = -cells * self.cell_size * (1.0 - drop_progress)
                color = jewel.value
                padding = 6
                if self.anim_state == "removing" and (i, j) in self.removing:
                    remove_progress = min(1.0, (now - self.remove_start) / self.remove_duration)
                    scale = 1.0 - remove_progress
                    if scale <= 0:
                        continue
                    half = self.cell_size // 2
                    size = int((self.cell_size - padding * 2) * scale)
                    cx = x + half
                    cy = y + half
                    rect = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
                else:
                    rect = pygame.Rect(
                        x + dx + padding,
                        y + dy + padding,
                        self.cell_size - padding * 2,
                        self.cell_size - padding * 2
                    )
                pygame.draw.rect(screen, color, rect, border_radius=8)
                cx = rect.centerx
                cy = rect.centery
                icon_font = pygame.font.Font(None, 28)

                if jewel == JEWEL.BOMB:
                    size = 12
                    bomb_rect = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
                    pygame.draw.rect(screen, (0, 0, 0), bomb_rect, border_radius=3)
                elif jewel == JEWEL.LINE:
                    pygame.draw.line(screen, (0, 0, 0), (rect.left + 4, cy),
                                     (rect.right - 4, cy), 3)
                    pygame.draw.line(screen, (0, 0, 0), (rect.left + 4, cy - 5),
                                     (rect.right - 4, cy - 5), 2)
                elif jewel == JEWEL.COLOR:
                    pygame.draw.line(screen, (0, 0, 0), (cx - 8, cy), (cx + 8, cy), 3)
                    pygame.draw.line(screen, (0, 0, 0), (cx, cy - 8), (cx, cy + 8), 3)
                    pygame.draw.line(screen, (0, 0, 0), (cx - 6, cy - 6),
                                     (cx + 6, cy + 6), 2)
                    pygame.draw.line(screen, (0, 0, 0), (cx + 6, cy - 6),
                                     (cx - 6, cy + 6), 2)
                if self.selected == (i, j):
                    pygame.draw.rect(screen, self.colors["white"], rect, 3, border_radius=8)
        panel_x = self.offset_x + self.board.column * self.cell_size + 15
        panel_y = self.offset_y
        font_label = pygame.font.Font(None, 36)
        font_value = pygame.font.Font(None, 46)
        label = font_label.render("Score", True, self.colors["white"])
        screen.blit(label, (panel_x, panel_y))
        value = font_value.render(str(self.score), True, self.colors["white"])
        screen.blit(value, (panel_x, panel_y + 35))

        if self.mode == "time":
            time_label = font_label.render("Time", True, self.colors["white"])
            screen.blit(time_label, (panel_x, panel_y + 110))
            seconds = max(0, int(self.time_left))
            time_str = f"{seconds // 60}:{seconds % 60:02d}"
            time_value = font_value.render(time_str, True, self.colors["white"])
            screen.blit(time_value, (panel_x, panel_y + 145))

        if self.mode == "score":
            moves_label = font_label.render("Moves", True, self.colors["white"])
            screen.blit(moves_label, (panel_x, panel_y + 110))
            moves_value = font_value.render(str(self.moves_left), True, self.colors["white"])
            screen.blit(moves_value, (panel_x, panel_y + 145))
            goal_label = font_label.render("Goal", True, self.colors["white"])
            screen.blit(goal_label, (panel_x, panel_y + 220))
            goal_value = font_value.render(str(self.goal), True, self.colors["yellow"])
            screen.blit(goal_value, (panel_x, panel_y + 255))

    def _calc_drop_offsets(self):
        offsets = {}
        for j in range(self.board.column):
            empty = 0
            for i in range(self.board.row - 1, -1, -1):
                if self.board.field[i][j] is None:
                    empty += 1
                elif empty > 0:
                    offsets[(i, j)] = empty
        return offsets

    def update(self):
        if self.mode == "time":
            now = pygame.time.get_ticks()
            self.time_left -= (now - self.last_tick) / 1000
            self.last_tick = now
        now = pygame.time.get_ticks()
        progress = min(1.0, (now - self.anim_start) / self.anim_duration)
        if self.anim_state == "swapping" and progress >= 1.0:
            r1, c1 = self.swap_from
            r2, c2 = self.swap_to
            jewel1 = self.board.field[r1][c1]
            jewel2 = self.board.field[r2][c2]
            self.board.field[r1][c1], self.board.field[r2][c2] = \
                self.board.field[r2][c2], self.board.field[r1][c1]
            extra = set()
            if jewel1 == JEWEL.BOMB:
                extra |= self.board.apply_bomb(r2, c2)
            if jewel2 == JEWEL.BOMB:
                extra |= self.board.apply_bomb(r1, c1)
            if jewel1 == JEWEL.LINE:
                extra |= self.board.apply_line(r2, c2)
            if jewel2 == JEWEL.LINE:
                extra |= self.board.apply_line(r1, c1)
            if jewel1 == JEWEL.COLOR:
                extra |= self.board.apply_color(r2, c2, jewel2)
            if jewel2 == JEWEL.COLOR:
                extra |= self.board.apply_color(r1, c1, jewel1)
            matches = self.board.find_matches()
            matches |= extra
            if matches:
                special = None
                center = list(matches)[len(matches) // 2]
                if (len(matches)) >= 5:
                    special = (center, JEWEL.COLOR)
                elif len(matches) == 4:
                    special = (center, JEWEL.BOMB)
                self.pending_special = special
                self.removing = matches
                self.remove_start = pygame.time.get_ticks()
                self.anim_state = "removing"
                if self.mode == "score":
                    self.moves_left -= 1
                self.score += len(matches) * self.points_per_jewel
            else:
                self.board.field[r1][c1], self.board.field[r2][c2] = \
                    self.board.field[r2][c2], self.board.field[r1][c1]
                self.anim_state = "idle"
        if self.anim_state == "removing":
            remove_progress = min(1.0, (now - self.remove_start) / self.remove_duration)
            if remove_progress >= 1.0:
                for i, j in self.removing:
                    self.board.field[i][j] = None
                self.removing = set()
                if self.pending_special:
                    (pi, pj), jewel_type = self.pending_special
                    self.board.field[pi][pj] = jewel_type
                    self.pending_special = None
                self.drop_offsets = self._calc_drop_offsets()
                self.board.drop_jewels()
                self.board.fill_empty()
                self.drop_start = pygame.time.get_ticks()
                self.anim_state = "dropping"
        if self.anim_state == "dropping":
            drop_progress = min(1.0, (now - self.drop_start) / self.drop_duration)
            if drop_progress >= 1.0:
                self.drop_offsets = {}
                matches = self.board.find_matches()
                if matches:
                    self.removing = matches
                    self.remove_start = pygame.time.get_ticks()
                    self.anim_state = "removing"
                    self.score += len(matches) * self.points_per_jewel
                else:
                    self.anim_state = "idle"

    def get_cell(self, mouse_x, mouse_y):
        col = (mouse_x - self.offset_x) // self.cell_size
        row = (mouse_y - self.offset_y) // self.cell_size
        if 0 <= row < self.board.row and 0 <= col < self.board.column:
            return (row, col)
        return None

    def start_swap(self, cell1, cell2):
        self.anim_state = "swapping"
        self.anim_start = pygame.time.get_ticks()
        self.swap_from = cell1
        self.swap_to = cell2

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.anim_state != "idle":
                return
            cell = self.get_cell(*event.pos)
            if cell is None:
                self.selected = None
                return
            if self.selected is None:
                self.selected = cell
            else:
                self.start_swap(self.selected, cell)
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
        config_color = ConfigColor()
        colors_raw = config_color.get("colors")
        self.colors = {key: tuple(value) for key, value in colors_raw.items()}
        screen_config = config.get("screen")
        self.width = screen_config["width"]
        self.height = screen_config["height"]
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 42)
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
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
        title = self.font_title.render("Game Over", True, (self.colors["white"]))
        screen.blit(title, title.get_rect(center=(self.width // 2, 100)))
        score_text = self.font_text.render(f"Score: {self.score}", True, (self.colors["white"]))
        screen.blit(score_text, score_text.get_rect(center=(self.width // 2, 200)))
        if self.is_record:
            record_text = self.font_text.render("New record!", True, (self.colors["white"]))
            screen.blit(record_text, record_text.get_rect(center=(self.width // 2, 280)))
            if self.input_activate:
                prompt = self.font_text.render("Your name: ", True, (200, 200, 200))
                screen.blit(prompt, prompt.get_rect(center=(self.width // 2, 350)))
                input_rect = pygame.Rect(self.width // 2 - 150, 390, 300, 50)
                pygame.draw.rect(screen, (50, 40, 90), input_rect, border_radius=8)
                pygame.draw.rect(screen, (150, 120, 200), input_rect, 2, border_radius=8)
                name_text = self.font_text.render(self.name_input, True, (self.colors["white"]))
                screen.blit(name_text, name_text.get_rect(center=input_rect.center))
                hint = self.font_button.render("Press Enter to save", True, (150, 150, 150))
                screen.blit(hint, hint.get_rect(center=(self.width // 2, 460)))
            else:
                saved = self.font_text.render("The record has been saved", True, (100, 255, 100))
                screen.blit(saved, saved.get_rect(center=(self.width // 2, 370)))
        mouse_pos = pygame.mouse.get_pos()
        for rect, label in [(self.menu_rect, "Back"), (self.retry_rect, "Play again")]:
            color = (80, 60, 120) if rect.collidepoint(mouse_pos) else (50, 40, 90)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (150, 120, 200), rect, 2, border_radius=8)
            text = self.font_button.render(label, True, (self.colors["white"]))
            screen.blit(text, text.get_rect(center=rect.center))