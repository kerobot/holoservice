import motor.motor_asyncio
from api.settings import get_mongo_settings

mongo_settings = get_mongo_settings()

def get_db():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.uri)
        db = client.get_database(mongo_settings.database)
        yield db
    finally:
        client.close()
