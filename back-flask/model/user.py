from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from dao.users_dao import UsersDAO, RequestersDAO, VolunteersDAO, ShopOwnersDAO
from db import db
from model.exception import UserNotFoundError, IncorrectPasswordError, UserAlreadyRegisteredError


class User(ABC):

    # in-memory storage of active user sessions, used to authenticate users in every further request after login
    active_user_sessions: Dict[str, User] = {}

    def __init__(self, login_name: str, password_hash: str, first_name: str, last_name: str, id: Optional[str] = None):
        self.login_name: str = login_name
        self.password_hash: str = password_hash
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.id: Optional[str] = id

    @classmethod
    @abstractmethod
    def get_dao(cls) -> UsersDAO:
        raise NotImplementedError

    @classmethod
    def from_db_object(cls, user_dict: Dict[str, Any]) -> User:
        return cls(
            login_name=user_dict['login']['name'],
            password_hash=user_dict['login']['passwordHash'],
            first_name=user_dict['name']['first'],
            last_name=user_dict['name']['last'],
            id=str(user_dict['_id'])
        )

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'login': {
                'name': self.login_name,
                'passwordHash': self.password_hash
            },
            'name': {
                'last': self.last_name,
                'first': self.first_name
            }
        }

    @classmethod
    def hash_password(cls, password: str) -> str:
        # TODO: use proper hashing function
        return password

    @classmethod
    def generate_session_id(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def add_active_user_session(cls, user: User) -> str:
        session_id = cls.generate_session_id()
        cls.active_user_sessions[session_id] = user
        return session_id

    @classmethod
    def login(cls, name: str, password: str) -> str:
        ''' Returns the session id for that user. The client is expected to send this session id with every further request. '''
        db_user = cls.get_dao().get_user_by_login_name(name)
        if db_user is None:
            raise UserNotFoundError
        user = cls.from_db_object(db_user)
        if not cls.hash_password(password) == user.password_hash:
            raise IncorrectPasswordError
        return cls.add_active_user_session(user)

    @classmethod
    def register(cls, login_name: str, password: str, first_name: str, last_name: str) -> str:
        ''' Returns the session id for that user. The client is expected to send this session id with every further request. '''
        if cls.get_dao().get_user_by_login_name(login_name) is not None:
            raise UserAlreadyRegisteredError
        user = cls(
            login_name=login_name,
            password_hash=cls.hash_password(password),
            first_name=first_name,
            last_name=last_name
        )
        id = cls.get_dao().store_user(user.to_db_object())
        user.id = id
        return cls.add_active_user_session(user)




class Requester(User):

    active_user_sessions: Dict[str, Requester] = {}

    @classmethod
    def get_dao(cls) -> RequestersDAO:
        return RequestersDAO(db)


class Volunteer(User):

    active_user_sessions: Dict[str, Volunteer] = {}

    @classmethod
    def get_dao(cls) -> VolunteersDAO:
        return VolunteersDAO(db)


class ShopOwner(User):

    active_user_sessions: Dict[str, ShopOwner] = {}

    @classmethod
    def get_dao(cls) -> ShopOwnersDAO:
        return ShopOwnersDAO(db)

