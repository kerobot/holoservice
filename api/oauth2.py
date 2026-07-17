from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt  # type: ignore[import-untyped]
from jose.exceptions import JWTError  # type: ignore[import-untyped]
from passlib.context import CryptContext  # type: ignore[import-untyped]
from passlib.exc import UnknownHashError  # type: ignore[import-untyped]
from api.repository.user import UserRepository
from api.schemas.token import TokenData
from api.settings import get_jwt_settings
from api.schemas.user import UserModel
from api.db import get_db
from api.exceptions import CredentialsException, InactiveUserException
from motor.core import AgnosticDatabase

jwt_settings = get_jwt_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password: str) -> str:
    # パスワードをハッシュ化する
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # パスワードが正しいかどうかを確認する
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # 旧データなどでハッシュ形式が不正な場合は認証失敗として扱う
        return False


async def authenticate_user(
    username: str,
    password: str,
    db: AgnosticDatabase = Depends(get_db),
) -> UserModel | None:
    # ユーザーを認証する
    user = await UserRepository.get_by_username(db, username)
    if not user:
        return None
    if user.password is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # アクセストークンを作成する
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=jwt_settings.exp_delta_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AgnosticDatabase = Depends(get_db),
) -> UserModel:
    # アクセストークンから現在のユーザーを非同期で取得する
    try:
        payload = jwt.decode(
            token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm]
        )
        username = payload.get("sub")
        if not isinstance(username, str):
            raise CredentialsException()
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException()

    if token_data.username is None:
        raise CredentialsException()

    user = await UserRepository.get_by_username(db, username=token_data.username)
    if user is None:
        raise CredentialsException()
    return user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    # 現在のユーザーが有効かどうかを確認する
    if current_user.disabled:
        if current_user.id is None:
            raise CredentialsException()
        raise InactiveUserException(identifier=current_user.id)
    return current_user
