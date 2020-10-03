from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database


class UsersDAO(object):

    @abstractmethod
    def __init__(self, db: Database, collection_name: str):
        self.db: Database = db
        self.collection: Collection = db.get_collection(collection_name)

    def get_user_by_login_name(self, name: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({'login.name': name})

    def store_user(self, user_dict: Dict[str, Any]) -> ObjectId:
        return self.collection.insert_one(user_dict)

    def clear(self) -> None:
        self.collection.delete_many({})


class RequestersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(RequestersDAO, self).__init__(db, 'Requesters')


class VolunteersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(VolunteersDAO, self).__init__(db, 'Volunteers')


class ShopOwnersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(ShopOwnersDAO, self).__init__(db, 'ShopOwners')
