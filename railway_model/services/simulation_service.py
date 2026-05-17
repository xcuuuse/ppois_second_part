from dataclasses import dataclass
from typing import List
from services.movement_service import MovementEvent
from services.timetable import Timetable
from management.timer import Timer
from services.movement_service import MovementService
from domain.exceptions.exceptions import TimetableError
from persistence.repositories import SimulationClock, PassengerRepository


@dataclass
class DepartureInfo:
    compound_id: int
    departure_time: int
    from_station: str
    status: str
    minutes_until: int


@dataclass
class TickResult:
    new_time: int
    movement_events: List[MovementEvent]
    departures: List[DepartureInfo]


class SimulationService:
    @staticmethod
    def upcoming_departures(timetable: Timetable, current_time: int):
        result: List[DepartureInfo] = []
        for cell in timetable.cells:
            departure = cell.time
            if departure == current_time:
                result.append(
                    DepartureInfo(
                        compound_id=cell.compound.compound_id,
                        departure_time=departure,
                        from_station=cell.route.stations[0].name,
                        status="departing",
                        minutes_until=0
                    )
                )
            elif current_time < departure <= current_time + 30:
                result.append(DepartureInfo(
                    compound_id=cell.compound.compound_id,
                    departure_time=departure,
                    from_station=cell.route.stations[0].name,
                    status="soon",
                    minutes_until=departure - current_time
                ))
            return result

    @staticmethod
    def tick(timetable: Timetable,
             minutes: int,
             clock: SimulationClock,
             passengers: PassengerRepository):
        new_time = clock.advance(minutes)
        movement_events: List[MovementEvent] = []
        for cell in timetable.cells:
            if cell.time <= new_time and cell.compound.current_pos < len(cell.route.stations) - 1:
                movement_events.extend(MovementService.move_compound(cell, passengers))
        return TickResult(
            new_time=new_time,
            movement_events=movement_events,
            departures=SimulationService.upcoming_departures(timetable, new_time)
        )

    @staticmethod
    def set_time(target_time: int, clock: SimulationClock):
        if target_time <= clock.now():
            raise TimetableError("You cant set time less than now")
        return clock.set_to(target_time)

    @staticmethod
    def now(timetable: Timetable, clock: SimulationClock):
        current = clock.now()
        return current, SimulationService.upcoming_departures(timetable, current)