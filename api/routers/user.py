from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pymongo import ReturnDocument
from api.oauth2 import get_current_user
from bson import ObjectId
from api.db import get_db
from api.repository.user import UserRepository
from api.schemas.user import UserModel, UserCollection

router = APIRouter(
    tags=['user']
)

@router.get("/users/{id}", response_model=UserModel, response_model_by_alias=False)
async def get_user(id: str, db = Depends(get_db)):
    return await UserRepository.get(db, id);

@router.get("/users", response_model=UserCollection, response_model_by_alias=False)
async def list_users(db = Depends(get_db)):
    return await UserRepository.list(db);

@router.post("/users", response_model=UserModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def create_user(user: UserModel = Body(...), 
                      db = Depends(get_db)):
    user_collection = db.get_collection("users")
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@router.put("/users/{id}", response_model=UserModel, response_model_by_alias=False)
async def update_user(id: str, 
                      user: UserModel = Body(...), 
                      db = Depends(get_db)):
    user_collection = db.get_collection("users")
    # ユーザーのキーと値を取得し、辞書内包表記を利用して値が None でない場合に user に格納する
    update_user = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }
    if len(update_user) >= 1:
        update_result = await user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_user},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")
    if (existing_user := await user_collection.find_one({"_id": id})) is not None:
        return existing_user
    raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.delete("/users/{id}")
async def delete_user(id: str, 
                      db = Depends(get_db)):
    user_collection = db.get_collection("users")
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"User {id} not found")
