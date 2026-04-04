from .gem import GemType
from .constants import COLS, ROWS


class Board:
    def __init__(self, layout):
        self.grid = [[None] * COLS for _ in range(ROWS)]
        self.active = [[False] * COLS for _ in range(ROWS)]
        self.golden = [[False] * COLS for _ in range(ROWS)]

