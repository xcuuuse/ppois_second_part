from dataclasses import dataclass
from domain.compound.coach import Coach
from services.timetable import Timetable, TimetableCell
from services.ticket_manager import TicketManager
from management.passenger_serializer import PassengerSerializer
from domain.exceptions.exceptions import SeatError, TimetableError
from persistence.repositories import PassengerRepository

@dataclass
class BookingResult:
    passenger_id: int
    compound_id: int
    coach_number: int
    seat_number: int
    departure_time: int
    route_from: str
    route_to: str


class BookingService:

    @staticmethod
    def _find_cell(timetable: Timetable, compound_id: int) -> TimetableCell:
        for cell in timetable.cells:
            if cell.compound.compound_id == compound_id:
                return cell
        raise TimetableError(f"Compound {compound_id} not found")

    @staticmethod
    def _validate_seat(coach: Coach, seat_number: int, pass_id: int):
        if seat_number not in coach.seats:
            raise SeatError(f"Seat {seat_number} does not exist in coach {coach.number}")
        if seat_number not in coach.free_seats:
            raise SeatError(f"Seat {seat_number} in coach {coach.number} is already occupied")
        if coach.seats[seat_number] == pass_id:
            raise SeatError(f"Passenger {pass_id} already occupies seat {seat_number}")

    @staticmethod
    def book_seat(timetable: Timetable,
                  compound_id: int,
                  coach_number: int,
                  seat_number: int,
                  passenger_id: int,
                  passengers: PassengerRepository) -> BookingResult:
        cell = BookingService._find_cell(timetable, compound_id)
        compound = cell.compound
        if coach_number < 1 or coach_number > len(compound.coaches):
            raise SeatError(f"Coach {coach_number} does not exist")
        coach = compound.coaches[coach_number - 1]
        BookingService._validate_seat(coach, seat_number, passenger_id)
        passenger = passengers.get(passenger_id, timetable)
        TicketManager.create_ticket(passenger, compound, coach, seat_number, cell.time)
        passengers.save(passenger)
        return BookingResult(
            passenger_id=passenger_id,
            compound_id=compound.compound_id,
            coach_number=coach.number,
            seat_number=seat_number,
            departure_time=cell.time,
            route_from=cell.route.stations[0].name,
            route_to=cell.route.stations[-1].name,
        )
