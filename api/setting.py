from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

class Settings(BaseSettings):
    app_name: str = "Holodule Service"
    mongodb_uri: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_exp_delta_minutes: int = 15

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    try:
        return Settings()
    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))        
