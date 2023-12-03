from urllib.parse import quote_plus
import motor.motor_asyncio
from api.setting import get_settings

settings = get_settings()
mongodb_user = quote_plus(settings.mongodb_user)
mongodb_password = quote_plus(settings.mongodb_password)
mongodb_host = settings.mongodb_host
mongodb_holoduledb = f"mongodb://{mongodb_user}:{mongodb_password}@{mongodb_host}/holoduledb"

def get_db():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_holoduledb)
        db = client.holoduledb
        yield db
    finally:
        client.close()
