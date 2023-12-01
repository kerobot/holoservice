from fastapi import APIRouter, Depends
from api.db import get_db
from api.schemas.schedule import Schedule
from api.schemas.schedules import ScheduleCollection

router = APIRouter()

@router.get("/schecules", response_model = ScheduleCollection)
async def get_schecules(date: str, db = Depends(get_db)):
    holodule_collection = db.get_collection("holodules")
    return ScheduleCollection(schedules = await holodule_collection.find({"datetime": {'$regex':'^'+date}}).sort("datetime", -1).to_list(1000))

@router.post("/schecules")
async def create_schecule():
    pass

@router.put("/schecules/{key}")
async def update_schecule():
    pass

@router.delete("/schecules/{key}")
async def delete_schecule():
    pass
