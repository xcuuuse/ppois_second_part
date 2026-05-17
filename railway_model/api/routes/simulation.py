from fastapi import APIRouter, Depends
from persistence.json_timetable_repository import JsonTimetableRepository
from persistence.json_passenger_repository import JsonPassengerRepository
from persistence.json_clock import JsonClock
from services.simulation_service import SimulationService
from api.dependencies import get_timetable_repo, get_passenger_repo, get_clock
from api.schemas import (
    TickRequest, TickResponse, SetTimeRequest, NowResponse,
    MovementEventResponse, DepartureResponse,
)

router = APIRouter(prefix="/simulation", tags=["simulation"])


def _to_departure_response(departure):
    return DepartureResponse(
        compound_id=departure.compound_id,
        departure_time=departure.departure_time,
        from_station=departure.from_station,
        status=departure.status,
        minutes_until=departure.minutes_until
    )


@router.post("/tick", response_model=TickResponse)
def tick(
        body: TickRequest,
        timetable_repo: JsonTimetableRepository = Depends(get_timetable_repo),
        passengers: JsonPassengerRepository = Depends(get_passenger_repo),
        clock: JsonClock = Depends(get_clock)
):
    timetable = timetable_repo.load()
    result = SimulationService.tick(timetable, body.minutes, clock, passengers)
    timetable_repo.save(timetable)
    return TickResponse(
        new_time=result.new_time,
        movement_events=[MovementEventResponse(**event.__dict__) for event in result.movement_events],
        departures=[_to_departure_response(departure) for departure in result.departures]
    )


@router.post("/time", response_model=dict)
def set_time(
        body: SetTimeRequest,
        clock: JsonClock = Depends(get_clock)
):
    new_time = SimulationService.set_time(body.time, clock)
    return {"new_time": new_time}


@router.get("/now", response_model=NowResponse)
def now(
        timetable_repo: JsonTimetableRepository = Depends(get_timetable_repo),
        clock: JsonClock = Depends(get_clock)
):
    timetable = timetable_repo.load()
    current, departures = SimulationService.now(timetable, clock)
    return NowResponse(
        current_time=current,
        departures=[_to_departure_response(departure) for departure in departures]
        
    )