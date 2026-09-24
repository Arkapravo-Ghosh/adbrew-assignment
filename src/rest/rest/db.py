import os

from pymongo import MongoClient
from pymongo.database import Database

SERVER_SELECTION_TIMEOUT_MS = 3000


def _build_client() -> MongoClient:
    uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
    return MongoClient(
        uri,
        serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
        tz_aware=True,
    )


client = _build_client()
db: Database = client[os.environ.get("MONGO_DB_NAME", "test_db")]
