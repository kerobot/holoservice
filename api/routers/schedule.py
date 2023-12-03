from fastapi import APIRouter, Body, Depends, status
from api.db import get_db
from api.schemas.schedule import Schedule
from api.schemas.schedules import ScheduleCollection

router = APIRouter()

@router.get("/schecules", response_model = ScheduleCollection)
async def get_schecules(date: str, db = Depends(get_db)):
    holodule_collection = db.get_collection("holodules")
    return ScheduleCollection(schedules = await holodule_collection.find({"datetime": {'$regex':'^'+date}}).sort("datetime", -1).to_list(1000))

@router.post("/schecules", response_model = Schedule, status_code=status.HTTP_201_CREATED)
async def create_schecule(schedule: Schedule = Body(...), db = Depends(get_db)):
    holodule_collection = db.get_collection("holodules")
    new_schedule = await holodule_collection.insert_one(
        schedule.model_dump(by_alias=True, exclude=["id"])
    )
    created_schedule = await holodule_collection.find_one(
        {"_id": new_schedule.inserted_id}
    )
    return created_schedule

@router.put("/schecules/{key}")
async def update_schecule():
    pass

@router.delete("/schecules/{key}")
async def delete_schecule():
    pass
