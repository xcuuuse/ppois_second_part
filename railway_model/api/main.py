from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.exceptions.exceptions import (
    SeatError,
    TimetableError,
    CreatingEntityError,
    TicketSellingError,
    InvalidStateError,
    LocomotiveUsingError
)
from api.routes import compounds, bookings, passengers, simulation, timetable

app = FastAPI(
    title="Railway model",
    version="1.0.0"
)
app.include_router(compounds.router)
app.include_router(bookings.router)
app.include_router(passengers.router)
app.include_router(simulation.router)
app.include_router(timetable.router)


def _error_response(status: int, error: str, detail: str):
    return JSONResponse(status_code=status, content={"error": error, "detail": detail})


@app.exception_handler(TimetableError)
async def handle_timetable_error(_: Request, exception: TimetableError):
    message = str(exception)
    if "not found" in message.lower():
        return _error_response(404, "not_found", message)
    return _error_response(400, "bad_request", message)


@app.exception_handler(SeatError)
async def handle_seat_error(_: Request, exception: SeatError):
    return _error_response(400, "seat_error", str(exception))


@app.exception_handler(TicketSellingError)
async def handle_ticket_error(_: Request, exception: TicketSellingError):
    return _error_response(400, "ticket_error", str(exception))


@app.exception_handler(CreatingEntityError)
async def handle_creating_error(_: Request, exception: CreatingEntityError):
    return _error_response(400, "creating_entity_error", str(exception))


@app.exception_handler(InvalidStateError)
async def handle_invalid_state(_: Request, exception: InvalidStateError):
    return _error_response(409, "invalid_state", str(exception))


@app.exception_handler(LocomotiveUsingError)
async def handle_locomotive_error(_: Request, exception: LocomotiveUsingError):
    return _error_response(409, "locomotive_broken", str(exception))


@app.get("/", tags=["meta"])
def root():
    return {
        "service": "Railway Model API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }




