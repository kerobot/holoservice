from bson import ObjectId
from pymongo import ReturnDocument
from motor.core import AgnosticDatabase
from api.schemas.streamer import StreamerModel, StreamerCollection
from api.exceptions import NotFoundException

class StreamerRepository:
    @staticmethod
    async def get_by_id(db: AgnosticDatabase, 
                        id: str) -> StreamerModel:
        streamer_collection = db.get_collection("streamers")
        # ウォルラス演算子を利用して user が None でない場合に user を返す
        if (streamer := await streamer_collection.find_one({"_id": ObjectId(id)})) is not None:
            return StreamerModel(**streamer)
        raise NotFoundException(identifier=id)

    @staticmethod
    async def get_by_streamername(db: AgnosticDatabase, 
                              streamername: str) -> StreamerModel:
        streamer_collection = db.get_collection("streamers")
        # ウォルラス演算子を利用して user が None でない場合に user を返す
        if (streamer := await streamer_collection.find_one({"name": streamername})) is not None:
            return StreamerModel(**streamer)
        raise NotFoundException(identifier=streamername)

    @staticmethod
    async def list(db: AgnosticDatabase) -> StreamerCollection:
        streamer_collection = db.get_collection("streamers")
        return StreamerCollection(streamers=await streamer_collection.find().to_list(1000))

    @staticmethod
    async def create(db: AgnosticDatabase, 
                     streamer: StreamerModel) -> StreamerModel:
        streamer_collection = db.get_collection("streamers")
        result = await streamer_collection.insert_one(
            streamer.model_dump(by_alias=True, exclude=["id"])
        )
        return await StreamerRepository.get_by_id(db, result.inserted_id)

    @staticmethod
    async def update(db: AgnosticDatabase, 
                     id: str, 
                     streamer: StreamerModel) -> StreamerModel:
        streamer_collection = db.get_collection("streamers")
        # ストリーマーのキーと値を取得し、辞書内包表記を利用して値が None でない場合に update_streamer に格納する
        update_streamer = {
            k: v for k, v in streamer.model_dump(by_alias=True).items() if v is not None
        }
        # 更新対象が存在する場合は更新する
        if len(update_streamer) >= 1:
            result = await streamer_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": update_streamer},
                return_document=ReturnDocument.AFTER, # 更新後のドキュメントを返す
            )
        if result is not None:
            return result
        else:
            raise NotFoundException(identifier=id)

    @staticmethod
    async def delete(db: AgnosticDatabase, 
                     id: str):
        streamer_collection = db.get_collection("streamers")
        result = await streamer_collection.delete_one({"_id": ObjectId(id)})
        if not result.deleted_count:
            raise NotFoundException(identifier=id)
