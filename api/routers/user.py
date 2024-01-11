from fastapi import APIRouter, Body, Depends, Response, status
from motor.core import AgnosticDatabase
from api.oauth2 import get_current_active_user, get_hashed_password
from api.db import get_db
from api.repository.user import UserRepository
from api.schemas.user import UserModel, UserCollection

router = APIRouter(
    tags=['user']
)

@router.get("/users/{id}", 
            response_model=UserModel, 
            response_model_by_alias=False)
async def get_user(id: str, 
                   db: AgnosticDatabase = Depends(get_db), 
                   current_user: str = Depends(get_current_active_user)) -> UserModel:
    return await UserRepository.get_by_id(db, id);

@router.get("/users", 
            response_model=UserCollection, 
            response_model_by_alias=False)
async def list_users(db: AgnosticDatabase = Depends(get_db), 
                     current_user: str = Depends(get_current_active_user)) -> UserCollection:
    return await UserRepository.list(db);

@router.post("/users", 
             response_model=UserModel, 
             status_code=status.HTTP_201_CREATED, 
             response_model_by_alias=False)
async def create_user(user: UserModel = Body(...), 
                      db: AgnosticDatabase = Depends(get_db), 
                      current_user: str = Depends(get_current_active_user)) -> UserModel:
    # パスワードのハッシュ化
    if user.password is not None:
        user.password = get_hashed_password(user.password)
    return await UserRepository.create(db, user);

@router.put("/users/{id}", 
            response_model=UserModel, 
            response_model_by_alias=False)
async def update_user(id: str, 
                      user: UserModel = Body(...), 
                      db: AgnosticDatabase = Depends(get_db), 
                      current_user: str = Depends(get_current_active_user)) -> UserModel:
    # パスワードのハッシュ化
    if user.password is not None:
        user.password = get_hashed_password(user.password)
    return await UserRepository.update(db, id, user);

@router.delete("/users/{id}")
async def delete_user(id: str, 
                      db: AgnosticDatabase = Depends(get_db), 
                      current_user: str = Depends(get_current_active_user)) -> Response:
    await UserRepository.delete(db, id);
    return Response(status_code=status.HTTP_204_NO_CONTENT)
