from datetime import datetime, timezone
from typing import List

from pymongo import ASCENDING
from pymongo.collection import Collection

from .entities import Todo


def _utc_now() -> datetime:
    # MongoDB stores dates with millisecond precision; truncate so the value
    # returned on create matches what is read back later.
    now = datetime.now(timezone.utc)
    return now.replace(microsecond=now.microsecond // 1000 * 1000)


class TodoRepository:
    """All MongoDB access for todos. Nothing outside this class touches the collection."""

    def __init__(self, collection: Collection):
        self._collection = collection

    def list_all(self) -> List[Todo]:
        documents = self._collection.find().sort("created_at", ASCENDING)
        return [self._to_entity(document) for document in documents]

    def create(self, description: str) -> Todo:
        document = {
            "description": description,
            "created_at": _utc_now(),
        }
        result = self._collection.insert_one(document)
        return self._to_entity({**document, "_id": result.inserted_id})

    def delete_all(self) -> int:
        return self._collection.delete_many({}).deleted_count

    @staticmethod
    def _to_entity(document: dict) -> Todo:
        return Todo(
            id=str(document["_id"]),
            description=document["description"],
            created_at=document["created_at"],
        )
