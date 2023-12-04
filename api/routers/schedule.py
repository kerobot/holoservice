from datetime import datetime, timedelta, date, time
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pymongo import ReturnDocument
from api.oauth2 import get_current_user
from bson import ObjectId
from api.db import get_db
from api.schemas.schedule import ScheduleModel
from api.schemas.schedules import ScheduleCollection

router = APIRouter(
    tags=['schedule']
)

@router.get("/schedules", response_model=ScheduleCollection, response_model_by_alias=False)
async def get_schedules(schedule_date: date, code: str = None, db = Depends(get_db), current_user: str = Depends(get_current_user)):
    schedule_collection = db.get_collection("schedules")
    start = datetime.combine(schedule_date, time())
    end = start + timedelta(days=1)
    filter_dict = {'$and':[{"streaming_at": {'$gte': start, '$lt': end}}]}
    if code is not None:
        filter_dict["$and"].append({"code": code})
    return ScheduleCollection(schedules=await schedule_collection.find(filter_dict).sort("streaming_at", -1).to_list(1000))

@router.get("/schedules/{id}", response_model=ScheduleModel, response_model_by_alias=False)
async def get_schedule(id: str, db = Depends(get_db)):
    schedule_collection = db.get_collection("schedules")
    if (schedule := await schedule_collection.find_one({"_id": ObjectId(id)})) is not None:
        return schedule
    raise HTTPException(status_code=404, detail=f"Schedule {id} not found")

@router.post("/schedules", response_model=ScheduleModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def create_schedule(schedule: ScheduleModel = Body(...), db = Depends(get_db)):
    schedule_collection = db.get_collection("schedules")
    new_schedule = await schedule_collection.insert_one(
        schedule.model_dump(by_alias=True, exclude=["id"])
    )
    created_schedule = await schedule_collection.find_one(
        {"_id": new_schedule.inserted_id}
    )
    return created_schedule

@router.put("/schedules/{id}", response_model=ScheduleModel, response_model_by_alias=False)
async def update_schedule(id: str, schedule: ScheduleModel = Body(...), db = Depends(get_db)):
    schedule_collection = db.get_collection("schedules")
    schedule = {
        k: v for k, v in schedule.model_dump(by_alias=True).items() if v is not None
    }
    if len(schedule) >= 1:
        update_result = await schedule_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": schedule},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Schedule {id} not found")
    if (existing_schedule := await schedule_collection.find_one({"_id": id})) is not None:
        return existing_schedule
    raise HTTPException(status_code=404, detail=f"Schedule {id} not found")

@router.delete("/schedules/{id}")
async def delete_schedule(id: str, db = Depends(get_db)):
    schedule_collection = db.get_collection("schedules")
    delete_result = await schedule_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Schedule {id} not found")
