from domain.exceptions.exceptions import CreatingEntityError
from dataclasses import dataclass, field
from typing import List, Optional
from domain.compound.compound import Compound, Locomotive, Coach
from domain.railway.route import Route, Railway
from domain.railway.station import Station
from services.validator import Validator
from services.timetable_manager import TimetableManager, Timetable, TimetableCell
from services.booking_service import BookingService

@dataclass
class CoachState:
    number: int
    seat_price: int
    free_seats: List[int]


@dataclass
class CompoundState:
    compound_id: int
    current_pos: int
    current_station: Optional[str]
    state_name: str
    coaches: List[CoachState] = field(default_factory=list)


@dataclass
class CreateCompound:
    compound_id: int
    route_from: str
    route_to: str
    departure_time: int


class CompoundService:
    @staticmethod
    def _build_compound(locomotive_number: int, coach_amount: int,
                        seats: int, price: int):
        Validator.validate({"locomotive_number": locomotive_number, "coach_amount": coach_amount},
            {
                "locomotive_number": (int, lambda x: x >= 0),
                "coach_amount": (int, lambda x: x > 0),
            },)
        locomotive = Locomotive(locomotive_number)
        coaches = [Coach(i + 1, seats, price) for i in range(coach_amount)]
        return Compound(locomotive, coaches)

    @staticmethod
    def create_compound(timetable: Timetable, locomotive_number: int,
                        coach_amount: int, end_station_name: str,
                        departure_time: int, seats: int = 10,
                        price: int = 25):
        for cell in timetable.cells:
            if cell.compound.locomotive.number == locomotive_number:
                raise CreatingEntityError(
                    f"The locomotive {locomotive_number} is already occupied"
                )
        compound = CompoundService._build_compound(locomotive_number, coach_amount, seats, price)
        start = Station("O")
        end = Station(end_station_name)
        route = Route([Railway({start, end}, 100)])
        TimetableManager.add_cell(timetable, TimetableCell(compound, route, departure_time))
        return CreateCompound(
            compound_id=compound.compound_id,
            route_from=start.name,
            route_to=end.name,
            departure_time=departure_time
        )

    @staticmethod
    def get_state(timetable: Timetable, compound_id: int):
        cell = BookingService._find_cell(timetable, compound_id)
        compound = cell.compound
        route = cell.route
        if compound.current_pos < len(route.stations):
            current_station = route.stations[compound.current_pos].name
        else:
            current_station = None
        coaches = [
            CoachState(
                number=c.number,
                seat_price=c.seat_price,
                free_seats=c.free_seats
            )
            for c in compound.coaches
        ]
        return CompoundState(
            compound_id=compound.compound_id,
            current_pos=compound.current_pos,
            current_station=current_station,
            state_name=compound.state.name,
            coaches=coaches,
        )
