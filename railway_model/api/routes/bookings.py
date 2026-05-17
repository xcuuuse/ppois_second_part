from fastapi import APIRouter, Depends
from persistence.json_timetable_repository import JsonTimetableRepository
from persistence.json_passenger_repository import JsonPassengerRepository
from services.booking_service import BookingService
from api.dependencies import get_timetable_repo, get_passenger_repo
from api.schemas import BookingResponse, BookSeatRequest

router = APIRouter(prefix="/compounds", tags=["bookings"])


@router.post("/{compound_id}/bookings", response_model=BookingResponse, status_code=201)
def book_seat(compound_id: int,
              body: BookSeatRequest,
              timetable_repo: JsonTimetableRepository = Depends(get_timetable_repo),
              passengers: JsonPassengerRepository = Depends(get_passenger_repo)):
    timetable = timetable_repo.load()
    result = BookingService.book_seat(timetable=timetable,
                                      compound_id=compound_id,
                                      coach_number=body.coach_number,
                                      seat_number=body.seat_number,
                                      passenger_id=body.passenger_id,
                                      passengers=passengers)
    timetable_repo.save(timetable)
    return BookingResponse(**result.__dict__)
