import motor.motor_asyncio
from api.settings import get_settings

settings = get_settings()

def get_db():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
        db = client.get_database(settings.mongo_database)
        yield db
    finally:
        client.close()
