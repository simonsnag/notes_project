from motor.motor_asyncio import AsyncIOMotorClient
from settings import mongo_settings


class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            mongo_settings.database_url, uuidRepresentation="standard"
        )


mongodb = MongoDB()
db = mongodb.client[mongo_settings.mongo_name]
note_collection = db.get_collection("note")
basket_collection = db.get_collection("basket")
