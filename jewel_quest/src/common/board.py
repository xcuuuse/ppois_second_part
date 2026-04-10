import random
JEWEL_TYPES = ["R", "G", "B", "Y", "P"]


class Board:
    def __init__(self, row: int, column: int):
        self.field = [[None] * column for _ in range(row)]
        self.row = row
        self.column = column

    def fill(self):
        for i in range(self.row):
            for j in range(self.column):
                forbidden = set()
                if j >= 2 and self.field[i][j - 1] == self.field[i][j - 2]:
                    forbidden.add(self.field[i][j - 1])
                if i >= 2 and self.field[i - 1][j] == self.field[i - 2][j]:
                    forbidden.add(self.field[i - 1][j])
                choices = [t for t in JEWEL_TYPES if t not in forbidden]
                self.field[i][j] = random.choice(choices)

    def swap(self, row: int, column: int, new_row: int, new_column: int):
        if abs(row - new_row) + abs(column - new_column) != 1:
            return False
        self.field[row][column], self.field[new_row][new_column] = (
            self.field[new_row][new_column], self.field[row][column])
        if not self.remove_matches():
            self.field[row][column], self.field[new_row][new_column] = (
                self.field[new_row][new_column], self.field[row][column])
            return False
        self.process()
        return True

    def find_matches(self):
        to_remove = set()
        for i in range(self.row):
            for j in range(self.column - 2):
                if self.field[i][j] == self.field[i][j + 1] == self.field[i][j + 2]:
                    to_remove.add((i, j))
                    to_remove.add((i, j + 1))
                    to_remove.add((i, j + 2))
        for i in range(self.row - 2):
            for j in range(self.column):
                if self.field[i][j] == self.field[i + 1][j] == self.field[i + 2][j]:
                    to_remove.add((i, j))
                    to_remove.add((i + 1, j))
                    to_remove.add((i + 2, j))
        return to_remove

    def remove_matches(self):
        to_remove = self.find_matches()
        for i, j in to_remove:
            self.field[i][j] = None
        return len(to_remove)

    def print_board(self):
        for i in range(self.row):
            for j in range(self.column):
                print(self.field[i][j], end=" ")
            print("\n")

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
                    self.field[i][j] = random.choice(JEWEL_TYPES)

    def process(self):
        while True:
            matches = self.find_matches()
            if not matches:
                break
            self.remove_matches()
            self.drop_jewels()
            self.fill_empty()

