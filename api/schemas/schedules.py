from pydantic import BaseModel
from api.schemas.schedule import Schedule

class ScheduleCollection(BaseModel):
    schedules: list[Schedule]
