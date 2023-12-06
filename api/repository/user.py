from bson import ObjectId
from pymongo import ReturnDocument
from api.schemas.user import UserModel, UserCollection
from api.exceptions import NotFoundException

class UserRepository:
    @staticmethod
    async def get_by_id(db, id: str, enabled_only: bool = False) -> UserModel:
        user_collection = db.get_collection("users")
        filter_dict = {"_id": ObjectId(id)}
        if enabled_only:
            filter_dict["disabled"] = False
        # ウォルラス演算子を利用して user が None でない場合に user を返す
        if (user := await user_collection.find_one(filter_dict)) is not None:
            return UserModel(**user)
        raise NotFoundException(identifier=id)

    @staticmethod
    async def get_by_name(db, name: str, enabled_only: bool = False) -> UserModel:
        user_collection = db.get_collection("users")
        filter_dict = {"username": name}
        if enabled_only:
            filter_dict["disabled"] = False
        # ウォルラス演算子を利用して user が None でない場合に user を返す
        if (user := await user_collection.find_one(filter_dict)) is not None:
            return UserModel(**user)
        raise NotFoundException(identifier=name)

    @staticmethod
    async def list(db) -> UserCollection:
        user_collection = db.get_collection("users")
        return UserCollection(users=await user_collection.find().to_list(1000))

    @staticmethod
    async def create(db, user: UserModel) -> UserModel:
        user_collection = db.get_collection("users")
        result = await user_collection.insert_one(
            user.model_dump(by_alias=True, exclude=["id"])
        )
        return await UserRepository.get_by_id(db, result.inserted_id)

    @staticmethod
    async def update(db, id: str, user: UserModel) -> UserModel:
        user_collection = db.get_collection("users")
        # ユーザーのキーと値を取得し、辞書内包表記を利用して値が None でない場合に update_user に格納する
        update_user = {
            k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
        }
        if len(update_user) >= 1:
            result = await user_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": update_user},
                return_document=ReturnDocument.AFTER, # 更新後のドキュメントを返す
            )
        if result is not None:
            return result
        else:
            raise NotFoundException(identifier=id)

    @staticmethod
    async def delete(db, id: str):
        user_collection = db.get_collection("users")
        result = await user_collection.delete_one({"_id": ObjectId(id)})
        if not result.deleted_count:
            raise NotFoundException(identifier=id)
