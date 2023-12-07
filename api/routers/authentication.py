from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from motor.core import AgnosticDatabase
from api.db import get_db
from api.exceptions import NotFoundException
from api.oauth2 import create_access_token
from api.repository.user import UserRepository
from api.schemas.user import UserModel

router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), 
                    db: AgnosticDatabase = Depends(get_db)) -> dict:
    user: UserModel = await UserRepository.get_by_username(db, request.username)
    if user.password != request.password:
        raise NotFoundException(message='Incorrect password')
    access_token: str = create_access_token(data={'sub': user.username})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
