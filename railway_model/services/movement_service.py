from dataclasses import dataclass
from typing import List
from services.timetable import TimetableCell
from persistence.repositories import PassengerRepository


@dataclass
class MovementEvent:
    compound_id: int
    kind: str
    station_name: str


class MovementService:
    @staticmethod
    def move_compound(cell: TimetableCell, passengers: PassengerRepository):
        events: List[MovementEvent] = []
        compound = cell.compound
        route = cell.route
        compound.locomotive.start_engine()
        compound.move_along_route(route)
        if compound.current_pos < len(route.stations):
            events.append(MovementEvent(
                compound_id=compound.compound_id,
                kind="arrived",
                station_name=route.stations[compound.current_pos].name
            ))
        if compound.current_pos == len(route.stations) - 1:
            compound.process_station_actions()
            passengers.remove_tickets_for_compound(compound.compound_id)
            events.append(MovementEvent(
                compound_id=compound.compound_id,
                kind="completed",
                station_name=route.stations[-1].name
            ))
        return events
