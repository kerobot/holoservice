import motor.motor_asyncio
from motor.core import AgnosticClient, AgnosticDatabase
from api.settings import get_mongo_settings

mongo_settings = get_mongo_settings()

def get_db() -> AgnosticDatabase:
    try:
        client: AgnosticClient = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.uri)
        db: AgnosticDatabase = client.get_database(mongo_settings.database)
        yield db
    finally:
        client.close()
