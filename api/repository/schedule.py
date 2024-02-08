from datetime import datetime, timedelta, date, time
from bson import ObjectId
from pymongo import ReturnDocument
from pymongo import DESCENDING
from pymongo import ASCENDING
from motor.core import AgnosticDatabase
from api.schemas.schedule import ScheduleModel, ScheduleCollection
from api.exceptions import NotFoundException

class ScheduleRepository:
    @staticmethod
    async def get_by_id(db: AgnosticDatabase, 
                        id: str) -> ScheduleModel:
        schedule_collection = db.get_collection("schedules")
        # ウォルラス演算子を利用して schedule が None でない場合に schedule を返す
        if (schedule := await schedule_collection.find_one({"_id": ObjectId(id)})) is not None:
            return schedule
        raise NotFoundException(identifier=id)

    @staticmethod
    async def list(db: AgnosticDatabase, 
                   sdate: date = None, 
                   edate: date = None,
                   codes: [] = None) -> ScheduleCollection:
        schedule_collection = db.get_collection("schedules")
        filter_dict = {}
        if sdate is not None and edate is not None:
            start = datetime.combine(sdate, time())
            end = datetime.combine(edate, time())
            filter_dict["streaming_at"] = {'$gte': start, '$lt': end}
        elif sdate is not None:
            start = datetime.combine(sdate, time())
            filter_dict["streaming_at"] = {'$gte': start}
        elif edate is not None:
            end = datetime.combine(edate, time())
            filter_dict["streaming_at"] = {'$lt': end}
        if codes is not None and len(codes) > 0:
            filter_dict["code"] = {"$in": codes}
        return ScheduleCollection(schedules=await schedule_collection.find(filter_dict)
                                  .sort("streaming_at", DESCENDING)
                                  .to_list(1000))

    @staticmethod
    async def create(db: AgnosticDatabase, 
                     schedule: ScheduleModel) -> ScheduleModel:
        schedule_collection = db.get_collection("schedules")
        result = await schedule_collection.insert_one(
            schedule.model_dump(by_alias=True, exclude=["id"])
        )
        return await ScheduleRepository.get_by_id(db, result.inserted_id)

    @staticmethod
    async def update(db: AgnosticDatabase, 
                     id: str, 
                     schedule: ScheduleModel) -> ScheduleModel:
        schedule_collection = db.get_collection("schedules")
        # ユーザーのキーと値を取得し、辞書内包表記を利用して値が None でない場合に update_schedule に格納する
        update_schedule = {
            k: v for k, v in schedule.model_dump(by_alias=True).items() if v is not None
        }
        if len(update_schedule) >= 1:
            result = await schedule_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": update_schedule},
                return_document=ReturnDocument.AFTER, # 更新後のドキュメントを返す
            )
        if result is not None:
            return result
        else:
            raise NotFoundException(identifier=id)

    @staticmethod
    async def delete(db: AgnosticDatabase, 
                     id: str):
        schedule_collection = db.get_collection("schedules")
        result = await schedule_collection.delete_one({"_id": ObjectId(id)})
        if not result.deleted_count:
            raise NotFoundException(identifier=id)
