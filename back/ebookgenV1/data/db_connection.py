from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "quicky"

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self._client = None
        self._db = None

    async def connect(self):
        self._client = AsyncIOMotorClient(self._uri)
        self._db = self._client[self._db_name]

    async def close(self):
        if self._client:
            self._client.close()

    @property
    def db(self) -> Database:
        if not self._db:
            raise RuntimeError("Database is not connected.")
        return self._db

# singleton
mongodb = MongoDB(MONGO_URI, DATABASE_NAME)
