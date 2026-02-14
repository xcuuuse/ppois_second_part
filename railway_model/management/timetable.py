from typing import List
from .timetable_cell import TimetableCell


class Timetable:
    def __init__(self):
        self.cells: List[TimetableCell] = []

    def add_cell(self, cell: TimetableCell):
        self.cells.append(cell)
        self.cells.sort(key= lambda t: t.time)

    def __repr__(self):
        return f"Timetable({len(self.cells)} entries)"

    def show_all(self):
        for cell in self.cells:
            print(cell)

