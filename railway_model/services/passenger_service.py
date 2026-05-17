from dataclasses import dataclass
from domain.passenger.passenger import Passenger
from persistence.repositories import PassengerRepository


@dataclass
class CreatePassengerResult:
    passenger_id: int
    name: str
    finance: str


class PassengerService:
    @staticmethod
    def create_passenger(name: str, finance: int, passengers: PassengerRepository):
        Passenger.id_counter = passengers.next_id()
        passenger = Passenger(name, finance)
        passengers.save(passenger)
        return CreatePassengerResult(
            passenger_id=passenger.passenger_id,
            name=passenger.name,
            finance=passenger.finance
        )