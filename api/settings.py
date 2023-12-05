from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class MongoSettings(BaseSettings):
    uri: str
    database: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix='mongo_')

class JwtSettings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    exp_delta_minutes: int = 15

    model_config = SettingsConfigDict(env_file=".env", env_prefix='jwt_')

# キャッシュしたMongoDB設定を取得する関数
@lru_cache
def get_mongo_settings():
    return MongoSettings()

# キャッシュしたJWT設定を取得する関数
@lru_cache
def get_jwt_settings():
    return JwtSettings()
