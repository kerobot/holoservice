from fastapi import APIRouter, Body, Depends, Response, status
from motor.core import AgnosticDatabase
from api.oauth2 import get_current_active_user
from api.db import get_db
from api.repository.streamer import StreamerRepository
from api.schemas.streamer import StreamerModel, StreamerCollection

router = APIRouter(
    tags=['streamer']
)

@router.get("/streamers/{id}", 
            response_model=StreamerModel, 
            response_model_by_alias=False)
async def get_streamer(id: str, 
                   db: AgnosticDatabase = Depends(get_db), 
                   current_user: str = Depends(get_current_active_user)) -> StreamerModel:
    return await StreamerRepository.get_by_id(db, id);

@router.get("/streamers", 
            response_model=StreamerCollection, 
            response_model_by_alias=False)
async def list_streamers(db: AgnosticDatabase = Depends(get_db), 
                     current_user: str = Depends(get_current_active_user)) -> StreamerCollection:
    return await StreamerRepository.list(db);

@router.post("/streamers", 
             response_model=StreamerModel, 
             status_code=status.HTTP_201_CREATED, 
             response_model_by_alias=False)
async def create_streamer(streamer: StreamerModel = Body(...), 
                      db: AgnosticDatabase = Depends(get_db), 
                      current_user: str = Depends(get_current_active_user)) -> StreamerModel:
    return await StreamerRepository.create(db, streamer);

@router.put("/streamers/{id}", 
            response_model=StreamerModel, 
            response_model_by_alias=False)
async def update_streamer(id: str, 
                      streamer: StreamerModel = Body(...), 
                      db: AgnosticDatabase = Depends(get_db), 
                      current_user: str = Depends(get_current_active_user)) -> StreamerModel:
    return await StreamerRepository.update(db, id, streamer);

@router.delete("/streamers/{id}")
async def delete_streamer(id: str, 
                      db: AgnosticDatabase = Depends(get_db), 
                      current_user: str = Depends(get_current_active_user)) -> Response:
    await StreamerRepository.delete(db, id);
    return Response(status_code=status.HTTP_204_NO_CONTENT)
