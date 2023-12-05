from bson import ObjectId
from api.schemas.user import UserModel, UserCollection
from api.exceptions import NotFoundException

class UserRepository:
    @staticmethod
    async def get(db, id: str) -> UserModel:
        user_collection = db.get_collection("users")
        # ウォルラス演算子を利用して user が None でない場合に user を返す
        if (user := await user_collection.find_one({"_id": ObjectId(id)})) is not None:
            return UserModel(**user)
        raise NotFoundException(identifier=id)

    @staticmethod
    async def list(db) -> UserCollection:
        user_collection = db.get_collection("users")
        return UserCollection(users=await user_collection.find().to_list(1000))

    # @staticmethod
    # def create(create: PersonCreate) -> PersonRead:
    #     """Create a person and return its Read object"""
    #     document = create.dict()
    #     document["created"] = document["updated"] = get_time()
    #     document["_id"] = get_uuid()
    #     # The time and id could be inserted as a model's Field default factory,
    #     # but would require having another model for Repository only to implement it

    #     result = collection.insert_one(document)
    #     assert result.acknowledged

    #     return PeopleRepository.get(result.inserted_id)

    # @staticmethod
    # def update(person_id: str, update: PersonUpdate):
    #     """Update a person by giving only the fields to update"""
    #     document = update.dict()
    #     document["updated"] = get_time()

    #     result = collection.update_one({"_id": person_id}, {"$set": document})
    #     if not result.modified_count:
    #         raise PersonNotFoundException(identifier=person_id)

    # @staticmethod
    # def delete(person_id: str):
    #     """Delete a person given its unique id"""
    #     result = collection.delete_one({"_id": person_id})
    #     if not result.deleted_count:
    #         raise PersonNotFoundException(identifier=person_id)