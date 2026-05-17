from persistence.json_timetable_repository import JsonTimetableRepository
from persistence.json_passenger_repository import JsonPassengerRepository
from persistence.json_clock import JsonClock


def get_timetable_repo():
    return JsonPassengerRepository()


def get_passenger_repo():
    return JsonPassengerRepository()


def get_clock():
    return JsonClock()

