from fastapi import APIRouter, Body, Depends, Response, status
from api.oauth2 import get_current_user
from api.db import get_db
from api.repository.user import UserRepository
from api.schemas.user import UserModel, UserCollection

router = APIRouter(
    tags=['user']
)

@router.get("/users/{id}", response_model=UserModel, response_model_by_alias=False)
async def get_user(id: str, db = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await UserRepository.get_by_id(db, id);

@router.get("/users", response_model=UserCollection, response_model_by_alias=False)
async def list_users(db = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await UserRepository.list(db);

@router.post("/users", response_model=UserModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def create_user(user: UserModel = Body(...), db = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await UserRepository.create(db, user);

@router.put("/users/{id}", response_model=UserModel, response_model_by_alias=False)
async def update_user(id: str, user: UserModel = Body(...), db = Depends(get_db), current_user: str = Depends(get_current_user)):
    return await UserRepository.update(db, id, user);

@router.delete("/users/{id}")
async def delete_user(id: str, db = Depends(get_db), current_user: str = Depends(get_current_user)):
    await UserRepository.delete(db, id);
    return Response(status_code=status.HTTP_204_NO_CONTENT)
