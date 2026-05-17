from fastapi import APIRouter, Depends
from persistence.json_timetable_repository import JsonTimetableRepository
from persistence.json_passenger_repository import JsonPassengerRepository
from services.booking_service import BookingService
from api.dependencies import get_timetable_repo, get_passenger_repo
from api.schemas import BookingResponse, BookSeatRequest

router = APIRouter(prefix="/compounds", tags=["bookings"])

@router.post("/{compound_id}/bookings", response_model=BookingResponse, status_code=201)
def book_seat():
    pass