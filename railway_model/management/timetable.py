from typing import List
from .timetable_cell import TimetableCell


class Timetable:
    def __init__(self):
        self.cells: List[TimetableCell] = []

    def show_all(self):
        for cell in self.cells:
            print(str(cell))

    def remove_cell(self, cell: TimetableCell):
        self.cells.remove(cell)

    def add_cell(self, cell: TimetableCell):
        self.cells.append(cell)
