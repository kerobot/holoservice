import motor.motor_asyncio
from motor.core import AgnosticClient, AgnosticDatabase
from api.settings import get_mongo_settings
from typing import Generator

mongo_settings = get_mongo_settings()

def get_db() -> Generator[AgnosticDatabase, None, None]:
    try:
        client: AgnosticClient = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.uri)
        db: AgnosticDatabase = client.get_database(mongo_settings.database)
        yield db
    finally:
        client.close()
