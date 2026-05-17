from fastapi import APIRouter, Depends
from api.schemas import CreatePassengerResponse, CreatePassengerRequest
from persistence.json_passenger_repository import JsonPassengerRepository
from api.dependencies import get_passenger_repo
from services.passenger_service import PassengerService

router = APIRouter(prefix="/passengers", tags=["passengers"])

@router.post("", response_model=CreatePassengerResponse, status_code=201)
def create_passenger(
        body: CreatePassengerRequest,
        passengers: JsonPassengerRepository = Depends(get_passenger_repo)
):
    result = PassengerService.create_passenger(body.name, body.finance, passengers)
    return CreatePassengerResponse(**result.__dict__)
