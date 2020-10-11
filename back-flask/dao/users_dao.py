from typing import Optional, Dict, Any

from pymongo.database import Database

from dao.abstract_dao import AbstractDAO


class UsersDAO(AbstractDAO):

    def get_user_by_login_name(self, name: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({'login.name': name})


class RequestersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(RequestersDAO, self).__init__(db, 'Requesters')


class VolunteersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(VolunteersDAO, self).__init__(db, 'Volunteers')


class ShopOwnersDAO(UsersDAO):

    def __init__(self, db: Database):
        super(ShopOwnersDAO, self).__init__(db, 'ShopOwners')
