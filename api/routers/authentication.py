from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from motor.core import AgnosticDatabase
from api.db import get_db
from api.exceptions import CredentialsException
from api.oauth2 import authenticate_user, create_access_token
from api.schemas.token import Token
from api.schemas.user import UserModel

router = APIRouter(
    tags=['authentication']
)

@router.post('/token', response_model=Token)
async def get_token(request: OAuth2PasswordRequestForm = Depends(), 
                    db: AgnosticDatabase = Depends(get_db)) -> dict:
    user: UserModel = await authenticate_user(request.username, request.password, db)
    if not user:
        raise CredentialsException(message='Incorrect username or password')
    access_token: str = create_access_token(data={'sub': user.username})
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
