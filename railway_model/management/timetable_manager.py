from .timetable_cell import TimetableCell
from .timetable import Timetable
from exceptions.exceptions import TimetableError


class TimetableManager:

    @staticmethod
    def add_cell(timetable: Timetable, cell: TimetableCell):
        if cell in timetable.cells:
            raise TimetableError("The error already exists")
        timetable.cells.append(cell)
        timetable.cells.sort(key=lambda t: t.time)

    @staticmethod
    def remove_cell(timetable: Timetable, cell: TimetableCell):
        if cell not in timetable.cells:
            raise TimetableError("The cell doesn't exist")
        timetable.cells.remove(cell)

