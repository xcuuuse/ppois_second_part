import random
from src.common.jewel import JEWEL


class Board:
    def __init__(self, row: int, column: int):
        self.field = [[None] * column for _ in range(row)]
        self.row = row
        self.column = column
        self.special = {JEWEL.BOMB, JEWEL.LINE, JEWEL.COLOR}
        self.regular = [jewel for jewel in JEWEL if jewel not in self.special]

    def fill(self):
        for i in range(self.row):
            for j in range(self.column):
                forbidden = set()
                if j >= 2 and self.field[i][j - 1] == self.field[i][j - 2]:
                    forbidden.add(self.field[i][j - 1])
                if i >= 2 and self.field[i - 1][j] == self.field[i - 2][j]:
                    forbidden.add(self.field[i - 1][j])
                choices = [t for t in self.regular if t not in forbidden]
                self.field[i][j] = random.choice(choices)

    def find_matches(self):
        to_remove = set()
        for i in range(self.row):
            for j in range(self.column - 2):
                if self.field[i][j] is not None and self.field[i][j] == self.field[i][j + 1] == self.field[i][j + 2]:
                    to_remove.add((i, j))
                    to_remove.add((i, j + 1))
                    to_remove.add((i, j + 2))
        for i in range(self.row - 2):
            for j in range(self.column):
                if self.field[i][j] is not None and self.field[i][j] == self.field[i + 1][j] == self.field[i + 2][j]:
                    to_remove.add((i, j))
                    to_remove.add((i + 1, j))
                    to_remove.add((i + 2, j))
        return to_remove

    def drop_jewels(self):
        for j in range(self.column):
            column = [self.field[i][j] for i in range(self.row)]
            filtered = [c for c in column if c is not None]
            new_column = [None] * (self.row - len(filtered)) + filtered
            for i in range(self.row):
                self.field[i][j] = new_column[i]

    def fill_empty(self):
        for i in range(self.row):
            for j in range(self.column):
                if self.field[i][j] is None:
                    if random.random() < 0.05:
                        self.field[i][j] = random.choice(list(self.special))
                    else:
                        self.field[i][j] = random.choice(list(self.regular))

    def apply_bomb(self, row: int, column: int):
        to_remove = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                ni, nj = row + i, column + j
                if 0 <= ni < self.row and 0 <= nj < self.column:
                    to_remove.add((ni, nj))
        return to_remove

    def apply_line(self, row, column):
        to_remove = set()
        for j in range(self.column):
            to_remove.add((row, j))
        return to_remove

    def apply_color(self, row, column, target_color):
        to_remove = set()
        for i in range(self.row):
            for j in range(self.column):
                if self.field[i][j] == target_color:
                    to_remove.add((i, j))
        return to_remove
