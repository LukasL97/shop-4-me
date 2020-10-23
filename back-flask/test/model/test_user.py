from unittest import TestCase

from dao.users_dao import UsersDAO
from model.exception import IncorrectPasswordError, UserNotFoundError, UserAlreadyRegisteredError, \
    UserSessionIdNotFoundError
from model.user import User, UserHandler
from test.mongodb_integration_test_setup import get_empty_local_test_db


class UserHandlerTest(TestCase):

    dummy_db_user = {'login': {'name': 'name', 'passwordHash': 'pw'}, 'name': {'last': 'last', 'first': 'first'}}

    db = get_empty_local_test_db(['User'])
    dao = UsersDAO(db, 'User')
    user_handler = UserHandler(User, dao)

    def setUp(self):
        self.dao.clear()
        self.user_handler.active_user_sessions.clear()

    def test_generate_different_session_ids(self):
        session_ids = []
        num_generated = 100
        for i in range(num_generated):
            session_ids.append(self.user_handler.generate_session_id())
        self.assertEqual(len(set(session_ids)), num_generated)

    def test_add_active_user_session(self):
        user_1 = self.user_handler.model_cls('name1', 'pw1', 'first', 'last')
        user_2 = self.user_handler.model_cls('name2', 'pw2', 'first', 'last')
        user_3 = self.user_handler.model_cls('name3', 'pw3', 'first', 'last')
        users = [user_1, user_2, user_3]
        session_ids = []
        for user in users:
            session_ids.append(self.user_handler.add_active_user_session(user))
        for session_id, user in zip(session_ids, users):
            self.assertEqual(self.user_handler.active_user_sessions[session_id], user)

    def test_login_with_correct_data(self):
        self.dao.store_one(self.dummy_db_user)
        session_id = self.user_handler.login('name', 'pw')
        self.assertIn(session_id, self.user_handler.active_user_sessions)

    def test_login_with_wrong_password(self):
        self.dao.store_one(self.dummy_db_user)
        with self.assertRaises(IncorrectPasswordError):
            self.user_handler.login('name', 'wrong_pw')
        self.assertEqual(len(self.user_handler.active_user_sessions), 0)

    def test_login_with_unknown_user(self):
        with self.assertRaises(UserNotFoundError):
            self.user_handler.login('name', 'pw')
        self.assertEqual(len(self.user_handler.active_user_sessions), 0)

    def test_registration_with_correct_data(self):
        session_id = self.user_handler.register('name', 'pw', 'first', 'last')
        self.assertIn(session_id, self.user_handler.active_user_sessions)

    def test_registration_with_already_existing_user(self):
        session_id = self.user_handler.register('name', 'pw', 'first', 'last')
        self.assertIn(session_id, self.user_handler.active_user_sessions)
        with self.assertRaises(UserAlreadyRegisteredError):
            self.user_handler.register('name', 'pw', 'first', 'last')
        self.assertEqual(len(self.user_handler.active_user_sessions), 1)

    def test_logout_loggedin_user(self):
        self.dao.store_one(self.dummy_db_user)
        session_id = self.user_handler.login('name', 'pw')
        self.assertIn(session_id, self.user_handler.active_user_sessions)
        self.user_handler.logout(session_id)
        self.assertNotIn(session_id, self.user_handler.active_user_sessions)

    def test_logout_with_unknown_session_id(self):
        session_id = 'someId'
        self.assertNotIn(session_id, self.user_handler.active_user_sessions)
        with self.assertRaises(UserSessionIdNotFoundError):
            self.user_handler.logout(session_id)
