from datetime import date
from fastapi import APIRouter, Body, Depends, Response, status
from motor.core import AgnosticDatabase
from api.oauth2 import get_current_active_user
from api.db import get_db
from api.repository.schedule import ScheduleRepository
from api.repository.streamer import StreamerRepository
from api.schemas.schedule import ScheduleModel, ScheduleCollection

router = APIRouter(
    tags=['schedule']
)

@router.get("/schedules/{id}", 
            response_model=ScheduleModel, 
            response_model_by_alias=False)
async def get_schedule(id: str, 
                       db: AgnosticDatabase = Depends(get_db), 
                       current_user: str = Depends(get_current_active_user)) -> ScheduleModel:
    return await ScheduleRepository.get_by_id(db, id)

@router.get("/schedules", 
            response_model=ScheduleCollection, 
            response_model_by_alias=False)
async def list_schedules(sdate: date = None, 
                         edate: date = None,
                         code: str = None, 
                         group: str = None,
                         db: AgnosticDatabase = Depends(get_db), 
                         current_user: str = Depends(get_current_active_user)) -> ScheduleCollection:
    codes = []
    if code is not None:
        codes.append(code)
    if group is not None:
        sc = await StreamerRepository.list(db, group)
        if len(sc.streamers) > 0:
            codes.extend([s.code for s in sc.streamers])
    return await ScheduleRepository.list(db, sdate, edate, codes)

@router.post("/schedules", 
             response_model=ScheduleModel, 
             status_code=status.HTTP_201_CREATED, 
             response_model_by_alias=False)
async def create_schedule(schedule: ScheduleModel = Body(...), 
                          db: AgnosticDatabase = Depends(get_db), 
                          current_user: str = Depends(get_current_active_user)) -> ScheduleModel:
    return await ScheduleRepository.create(db, schedule)

@router.put("/schedules/{id}", 
            response_model=ScheduleModel, 
            response_model_by_alias=False)
async def update_schedule(id: str, 
                          schedule: ScheduleModel = Body(...), 
                          db: AgnosticDatabase = Depends(get_db), 
                          current_user: str = Depends(get_current_active_user)) -> ScheduleModel:
    return await ScheduleRepository.update(db, id, schedule)

@router.delete("/schedules/{id}")
async def delete_schedule(id: str, 
                          db: AgnosticDatabase = Depends(get_db), 
                          current_user: str = Depends(get_current_active_user)) -> Response:
    await ScheduleRepository.delete(db, id);
    return Response(status_code=status.HTTP_204_NO_CONTENT)
