from unittest import TestCase

from pymongo.database import Database

from dao.users_dao import UsersDAO
from model.exception import IncorrectPasswordError, UserNotFoundError, UserAlreadyRegisteredError, \
    UserSessionIdNotFoundError
from model.user import User
from test.mongodb_integration_test_setup import get_empty_local_test_db


class DummyUser(User):

    @classmethod
    def get_dao(cls) -> UsersDAO:
        return UserTest.DummyUsersDAO(UserTest.db)


class UserTest(TestCase):

    dummy_db_user = {'login': {'name': 'name', 'passwordHash': 'pw'}, 'name': {'last': 'last', 'first': 'first'}}

    db = get_empty_local_test_db(['DummyUser'])

    class DummyUsersDAO(UsersDAO):

        def __init__(self, db: Database):
            super().__init__(db, 'DummyUser')

    def setUp(self):
        DummyUser.get_dao().clear()
        DummyUser.active_user_sessions.clear()

    def test_generate_different_session_ids(self):
        session_ids = []
        num_generated = 100
        for i in range(num_generated):
            session_ids.append(User.generate_session_id())
        self.assertEqual(len(set(session_ids)), num_generated)

    def test_add_active_user_session(self):
        user_1 = DummyUser('name1', 'pw1', 'first', 'last')
        user_2 = DummyUser('name2', 'pw2', 'first', 'last')
        user_3 = DummyUser('name3', 'pw3', 'first', 'last')
        users = [user_1, user_2, user_3]
        session_ids = []
        for user in users:
            session_ids.append(User.add_active_user_session(user))
        for session_id, user in zip(session_ids, users):
            self.assertEqual(User.active_user_sessions[session_id], user)

    def test_login_with_correct_data(self):
        DummyUser.get_dao().store_one(self.dummy_db_user)
        session_id = DummyUser.login('name', 'pw')
        self.assertIn(session_id, DummyUser.active_user_sessions)

    def test_login_with_wrong_password(self):
        DummyUser.get_dao().store_one(self.dummy_db_user)
        with self.assertRaises(IncorrectPasswordError):
            DummyUser.login('name', 'wrong_pw')
        self.assertEqual(len(DummyUser.active_user_sessions), 0)

    def test_login_with_unknown_user(self):
        with self.assertRaises(UserNotFoundError):
            DummyUser.login('name', 'pw')
        self.assertEqual(len(DummyUser.active_user_sessions), 0)

    def test_registration_with_correct_data(self):
        session_id = DummyUser.register('name', 'pw', 'first', 'last')
        self.assertIn(session_id, DummyUser.active_user_sessions)

    def test_registration_with_already_existing_user(self):
        session_id = DummyUser.register('name', 'pw', 'first', 'last')
        self.assertIn(session_id, DummyUser.active_user_sessions)
        with self.assertRaises(UserAlreadyRegisteredError):
            DummyUser.register('name', 'pw', 'first', 'last')
        self.assertEqual(len(DummyUser.active_user_sessions), 1)

    def test_logout_loggedin_user(self):
        DummyUser.get_dao().store_one(self.dummy_db_user)
        session_id = DummyUser.login('name', 'pw')
        self.assertIn(session_id, DummyUser.active_user_sessions)
        DummyUser.logout(session_id)
        self.assertNotIn(session_id, DummyUser.active_user_sessions)

    def test_logout_with_unknown_session_id(self):
        session_id = 'someId'
        self.assertNotIn(session_id, DummyUser.active_user_sessions)
        with self.assertRaises(UserSessionIdNotFoundError):
            DummyUser.logout(session_id)
