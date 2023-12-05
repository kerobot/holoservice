from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Holodule Service"
    mongo_uri: str
    mongo_database: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_exp_delta_minutes: int = 15

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()
