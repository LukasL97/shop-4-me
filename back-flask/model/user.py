from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any

from dao.users_dao import UsersDAO, RequestersDAO, VolunteersDAO, ShopOwnersDAO
from db import db
from model.exception import UserNotFoundError, IncorrectPasswordError


class User(ABC):

    # in-memory storage of active user sessions, used to authenticate users in every further request after login
    active_user_sessions: Dict[str, User] = {}

    def __init__(self, name: str, password_hash: str):
        self.name: str = name
        self.password_hash: str = password_hash

    @classmethod
    @abstractmethod
    def get_dao(cls) -> UsersDAO:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, user_dict: Dict[str, Any]) -> User:
        return cls(user_dict['login']['name'], user_dict['login']['passwordHash'])

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
        db_user = cls.get_dao().get_user_by_name(name)
        if db_user is None:
            raise UserNotFoundError
        user = cls.from_dict(db_user)
        if not cls.hash_password(password) == user.password_hash:
            raise IncorrectPasswordError
        return cls.add_active_user_session(user)


class Requester(User):

    @classmethod
    def get_dao(cls) -> RequestersDAO:
        return RequestersDAO(db)


class Volunteer(User):

    @classmethod
    def get_dao(cls) -> VolunteersDAO:
        return VolunteersDAO(db)


class ShopOwner(User):

    @classmethod
    def get_dao(cls) -> ShopOwnersDAO:
        return ShopOwnersDAO(db)

