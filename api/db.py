import motor.motor_asyncio
from api.setting import get_settings

settings = get_settings()

def get_db():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_uri)
        db = client.holoduledb
        yield db
    finally:
        client.close()
