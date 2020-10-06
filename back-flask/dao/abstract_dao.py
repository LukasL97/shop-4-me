from abc import abstractmethod, ABC
from typing import Dict, Any, List

from pymongo.collection import Collection
from pymongo.database import Database


class AbstractDAO(ABC):

    @abstractmethod
    def __init__(self, db: Database, collection_name: str):
        self.db: Database = db
        self.collection: Collection = db.get_collection(collection_name)

    def clear(self) -> None:
        self.collection.delete_many({})

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({}))

    def store_one(self, object_dict: Dict[str, Any]) -> str:
        result = self.collection.insert_one(object_dict)
        return str(result.inserted_id)
