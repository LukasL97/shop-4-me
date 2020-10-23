from typing import Optional, Dict, Any

from bson import ObjectId
from pymongo.database import Database

from dao.abstract_dao import AbstractDAO


class UsersDAO(AbstractDAO):

    def __init__(self, db: Database, collection_name: str):
        super().__init__(db, collection_name)

    def get_user_by_login_name(self, name: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({'login.name': name})


class RequestersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(RequestersDAO, self).__init__(db, 'Requesters')

    def update_address(self, id: str, address: Dict[str, Any]) -> None:
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': {'address': address}})


class VolunteersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(VolunteersDAO, self).__init__(db, 'Volunteers')


class ShopOwnersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(ShopOwnersDAO, self).__init__(db, 'ShopOwners')
