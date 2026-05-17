from management.passenger_serializer import PassengerSerializer
from services.timetable import Timetable
from domain.passenger.passenger import Passenger


class JsonPassengerRepository:
    def __init__(self, path: str = PassengerSerializer.PASSENGERS_FILE):
        self._path = path

    def get(self, passenger_id: int, timetable: Timetable):
        return PassengerSerializer.get_passenger(passenger_id, timetable, self._path)

    def save(self, passenger: Passenger):
        PassengerSerializer.save_passenger(passenger, self._path)

    def remove_tickets_for_compound(self, compound_id: int):
        PassengerSerializer.remove_tickets_for_compound(compound_id, self._path)

    def next_id(self):
        data = PassengerSerializer.load_passengers(self._path)
        return data.get("id_counter", 1)

