from management.serializer import Serializer
from services.timetable import Timetable


class JsonTimetableRepository:
    def __init__(self, path: str = Serializer.STATE_FILE):
        self._path = path

    def load(self):
        try:
            return Serializer.load_state(self._path)
        except FileNotFoundError:
            return Timetable()

    def save(self, timetable: Timetable):
        Serializer.save_state(timetable, self._path)