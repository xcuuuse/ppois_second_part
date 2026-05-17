from fastapi import APIRouter, Depends
from api.dependencies import get_timetable_repo
from persistence.json_timetable_repository import JsonTimetableRepository
from services.compound_service import CompoundService
from api.schemas import (
    CreateCompoundRequest,
    CreatePassengerResponse,
    CoachStateResponse,
    CompoundStateResponse,
    CreateCompoundResponse
)

router = APIRouter(prefix="/compounds", tags=["compounds"])


@router.post("", response_model=CreateCompoundResponse, status_code=201)
def create_compound(
        body: CreateCompoundRequest,
        timetable_repo: JsonTimetableRepository = Depends(get_timetable_repo)

):
    timetable = timetable_repo.load()
    result = CompoundService.create_compound(
        timetable=timetable,
        locomotive_number=body.locomotive_number,
        coach_amount=body.coach_amount,
        end_station_name=body.end_station,
        departure_time=body.departure_time,
        seats=body.seats,
        price=body.price
    )
    timetable_repo.save(timetable)
    return CreateCompoundResponse(
        compound_id=result.compound_id,
        route_from=result.route_from,
        route_to=result.route_to,
        departure_time=result.departure_time
    )

@router.get("/{compound_id}", response_model=CompoundStateResponse)
def get_compound_state(
        compound_id: int,
        timetable_repo: JsonTimetableRepository = Depends(get_timetable_repo)):
    timetable = timetable_repo.load()
    state = CompoundService.get_state(timetable, compound_id)
    return CompoundStateResponse(
        compound_id=compound_id,
        current_pos=state.current_pos,
        current_station=state.current_station,
        state_name=state.state_name,
        coaches=[
            CoachStateResponse(
                number=coach.number,
                seat_price=coach.seat_price,
                free_seats=coach.free_seats
            )
            for coach in state.coaches
        ]
    )