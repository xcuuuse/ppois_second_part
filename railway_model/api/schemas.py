from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class CreateCompoundRequest(BaseModel):
    locomotive_number: int = Field(ge=0)
    coach_amount: int = Field(gt=0)
    departure_time: int = Field(ge=0, le=1439)
    end_station: str = Field(min_length=1)
    seats: int = Field(default=10, gt=0)
    price: int = Field(default=25, gt=0)


class CreateCompoundResponse(BaseModel):
    compound_id: int
    route_from: str
    route_to: str
    departure_time: int


class CoachStateResponse(BaseModel):
    number: int
    seat_price: int
    free_seats: List[int]


class CompoundStateResponse(BaseModel):
    compound_id: int
    current_pos: int
    current_station: Optional[str]
    state_name: str
    coaches: List[CoachStateResponse]

class BookSeatRequest(BaseModel):
    coach_number: int = Field(gt=0)
    seat_number: int = Field(gt=0)
    passenger_id: int = Field(gt=0)


class BookingResponse(BaseModel):
    passenger_id: int
    compound_id: int
    coach_number: int
    seat_number: int
    departure_time: int
    route_from: str
    route_to: str


class CreatePassengerRequest(BaseModel):
    name: str = Field(min_length=1)
    finance: int = Field(ge=0)


class CreatePassengerResponse(BaseModel):
    passenger_id: int
    name: str
    finance: int


class TickRequest(BaseModel):
    minutes: int = Field(default=30, gt=0)


class SetTimeRequest(BaseModel):
    time: int = Field(ge=0, le=1439)


class MovementEventResponse(BaseModel):
    compound_id: int
    kind: Literal["arrived", "completed"]
    station_name: str


class DepartureResponse(BaseModel):
    compound_id: int
    departure_time: int
    from_station: str
    status: Literal["departing", "soon"]
    minutes_until: int


class TickResponse(BaseModel):
    new_time: int
    movement_events: List[MovementEventResponse]
    departures: List[DepartureResponse]


class NowResponse(BaseModel):
    current_time: int
    departures: List[DepartureResponse]


class TimetableEntryResponse(BaseModel):
    compound_id: int
    route_from: str
    route_to: str
    departure_time: str


class TimetableResponse(BaseModel):
    entries: List[TimetableEntryResponse]


class ErrorResponse(BaseModel):
    error: str
    detail: str

