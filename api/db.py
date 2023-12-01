from urllib.parse import quote_plus
import motor.motor_asyncio

mongodb_user = "owner"
mongodb_password = "password"
mongodb_host = "localhost:27017"
mongodb_holoduledb = f"mongodb://{quote_plus(mongodb_user)}:{quote_plus(mongodb_password)}@{mongodb_host}/holoduledb"

def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_holoduledb)
    db = client.holoduledb
    yield db
    client.close()
