from pydantic import BaseModel
from api.schemas.schedule import ScheduleModel

class ScheduleCollection(BaseModel):
    schedules: list[ScheduleModel]
