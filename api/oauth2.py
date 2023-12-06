from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from api.repository.user import UserRepository
from api.settings import get_jwt_settings
from api.schemas.user import UserModel
from api.db import get_db
from api.exceptions import CredentialsException

jwt_settings = get_jwt_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# アクセストークンを作成する関数
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=jwt_settings.exp_delta_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)
    return encoded_jwt

# アクセストークンから現在のユーザーを取得する非同期関数
async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    try:
        payload = jwt.decode(token, jwt_settings.secret_key, algorithms=jwt_settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
    except JWTError:
        raise CredentialsException()
    return await UserRepository.get_by_name(db, username, enabled_only=True)
