from fastapi import APIRouter, Depends
from persistence.json_timetable_repository import JsonTimetableRepository
from api.dependencies import get_timetable_repo
from api.schemas import TimetableResponse, TimetableEntryResponse

router = APIRouter(prefix="/timetable", tags=["timetable"])


@router.get("", response_model=TimetableResponse)
def get_timetable(
        timetable_repo: JsonTimetableRepository = Depends(get_timetable_repo)
):
    timetable = timetable_repo.load()
    return TimetableResponse(
        entries=[
            TimetableEntryResponse(
                compound_id=cell.compound.compound_id,
                route_from=cell.route.stations[0].name,
                route_to=cell.route.stations[-1].name,
                departure_time=cell.time
            )
            for cell in timetable.cells
        ]
    )