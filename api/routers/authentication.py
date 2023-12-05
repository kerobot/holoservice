from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from api.db import get_db
from api.oauth2 import create_access_token
from api.schemas.user import UserModel

router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user_collection = db.get_collection("users")
    filter_dict = {'$and': [{"username": request.username},{"disabled": False}]}
    user = await user_collection.find_one(filter_dict)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials'
        )

    searched_user = UserModel(**user)
    if searched_user.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password'
        )

    access_token = create_access_token(data={'sub': searched_user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': searched_user.id,
        'username': searched_user.username
    }
