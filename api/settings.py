from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class MongoSettings(BaseSettings):
    uri: str
    database: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix='mongo_', extra="ignore")

class JwtSettings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    exp_delta_minutes: int = 15
    model_config = SettingsConfigDict(env_file=".env", env_prefix='jwt_', extra="ignore")

@lru_cache
def get_mongo_settings() -> MongoSettings:
    # キャッシュしたMongoDB設定を取得する
    return MongoSettings()

@lru_cache
def get_jwt_settings() -> JwtSettings:
    # キャッシュしたJWT設定を取得する
    return JwtSettings()
