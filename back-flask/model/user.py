from __future__ import annotations

import uuid
from typing import Dict, Any, Optional, Type, cast

from injector import inject

from dao.users_dao import UsersDAO, RequestersDAO, VolunteersDAO, ShopOwnersDAO
from model.abstract_model import AbstractModel, AbstractHandler
from model.exception import UserNotFoundError, IncorrectPasswordError, UserAlreadyRegisteredError, \
    UserSessionIdNotFoundError, UnexpectedUserTypeError
from model.location.address import Address


class UserHandlerResolver(object):

    @inject
    def __init__(self, requester_handler: RequesterHandler, volunteer_handler: VolunteerHandler, shop_owner_handler: ShopOwnerHandler):
        self.requester_handler: RequesterHandler = requester_handler
        self.volunteer_handler: VolunteerHandler = volunteer_handler
        self.shop_owner_handler: ShopOwnerHandler = shop_owner_handler

    def get(self, user_type: str) -> UserHandler:
        if user_type == 'Requester': return self.requester_handler
        if user_type == 'Volunteer': return self.volunteer_handler
        if user_type == 'ShopOwner': return self.shop_owner_handler
        raise UnexpectedUserTypeError


class User(AbstractModel):

    def __init__(self, login_name: str, password_hash: str, first_name: str, last_name: str, id: Optional[str] = None):
        self.login_name: str = login_name
        self.password_hash: str = password_hash
        self.first_name: str = first_name
        self.last_name: str = last_name
        super(User, self).__init__(id)

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


class UserHandler(AbstractHandler):

    @inject
    def __init__(self, model_cls: Type[User], dao: UsersDAO):
        self.active_user_sessions: Dict[str, User] = {}
        self.model_cls = model_cls
        self.dao: UsersDAO = dao
        super().__init__(model_cls, dao)

    def from_db_object(self, db_object: Dict[str, Any]) -> User:
        return self.model_cls(
            login_name=db_object['login']['name'],
            password_hash=db_object['login']['passwordHash'],
            first_name=db_object['name']['first'],
            last_name=db_object['name']['last'],
            id=str(db_object['_id'])
        )

    def hash_password(self, password: str) -> str:
        # TODO: use proper hashing function
        return password

    def generate_session_id(self) -> str:
        return str(uuid.uuid4())

    def add_active_user_session(self, user: User) -> str:
        session_id = self.generate_session_id()
        self.active_user_sessions[session_id] = user
        return session_id

    def get_user_id_from_session_id(self, session_id: str) -> str:
        try:
            return self.active_user_sessions[session_id].id
        except KeyError:
            raise UserSessionIdNotFoundError

    def login(self, name: str, password: str) -> str:
        ''' Returns the session id for that user. The client is expected to send this session id with every further request. '''
        db_user = self.dao.get_user_by_login_name(name)
        if db_user is None:
            raise UserNotFoundError
        user = self.from_db_object(db_user)
        if not self.hash_password(password) == user.password_hash:
            raise IncorrectPasswordError
        return self.add_active_user_session(user)

    def register(self, login_name: str, password: str, first_name: str, last_name: str) -> str:
        ''' Returns the session id for that user. The client is expected to send this session id with every further request. '''
        if self.dao.get_user_by_login_name(login_name) is not None:
            raise UserAlreadyRegisteredError
        user = self.model_cls(
            login_name=login_name,
            password_hash=self.hash_password(password),
            first_name=first_name,
            last_name=last_name
        )
        id = self.dao.store_one(user.to_db_object())
        user.id = id
        return self.add_active_user_session(user)

    def logout(self, session_id: str) -> str:
        if session_id in self.active_user_sessions:
            self.active_user_sessions.pop(session_id)
            return 'User logged out successfully'
        else:
            raise UserSessionIdNotFoundError


class Requester(User):

    def __init__(self, login_name: str, password_hash: str, first_name: str, last_name: str, id: Optional[str] = None, address: Optional[Address] = None):
        self.address: Optional[Address] = None
        super(Requester, self).__init__(login_name, password_hash, first_name, last_name, id)

    def to_db_object(self) -> Dict[str, Any]:
        db_obj = super(Requester, self).to_db_object()
        db_obj['address'] = None if self.address is None else self.address.to_db_object()
        return db_obj


class RequesterHandler(UserHandler):

    @inject
    def __init__(self, dao: RequestersDAO):
        self.dao = dao
        self.model_cls: Type[Requester] = Requester
        super().__init__(self.model_cls, self.dao)

    def from_db_object(self, db_object: Dict[str, Any]) -> Requester:
        requester = cast(Requester, super(RequesterHandler, self).from_db_object(db_object))
        if 'address' in db_object and db_object['address'] is not None:
            requester.address = Address.from_db_object(db_object['address'])
        return requester


class Volunteer(User):
    pass


class VolunteerHandler(UserHandler):

    @inject
    def __init__(self, dao: VolunteersDAO):
        self.dao: VolunteersDAO = dao
        self.model_cls: Type[Volunteer] = Volunteer
        super().__init__(self.model_cls, self.dao)


class ShopOwner(User):
    pass


class ShopOwnerHandler(UserHandler):

    @inject
    def __init__(self, dao: ShopOwnersDAO):
        self.dao: ShopOwnersDAO = dao
        self.model_cls: Type[ShopOwner] = ShopOwner
        super().__init__(self.model_cls, self.dao)
