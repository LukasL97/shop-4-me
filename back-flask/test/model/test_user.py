from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from dao.users_dao import UsersDAO
from model.exception import IncorrectPasswordError, UserNotFoundError
from model.user import User


class UserTest(TestCase):

    usersDAOMock = Mock(spec=UsersDAO)

    class DummyUser(User):

        @classmethod
        def get_dao(cls) -> UsersDAO:
            return UserTest.usersDAOMock

    def setUp(self):
        UserTest.usersDAOMock.reset_mock()

    def test_generate_different_session_ids(self):
        session_ids = []
        num_generated = 100
        for i in range(num_generated):
            session_ids.append(User.generate_session_id())
        self.assertEqual(len(set(session_ids)), num_generated)

    def test_add_active_user_session(self):

        user_1 = UserTest.DummyUser('name1', 'pw1')
        user_2 = UserTest.DummyUser('name2', 'pw2')
        user_3 = UserTest.DummyUser('name3', 'pw3')
        users = [user_1, user_2, user_3]
        session_ids = []
        for user in users:
            session_ids.append(User.add_active_user_session(user))
        for session_id, user in zip(session_ids, users):
            self.assertEqual(User.active_user_sessions[session_id], user)

    def test_login_with_correct_data(self):
        UserTest.usersDAOMock.get_user_by_name.return_value = {'login': {'name': 'name', 'passwordHash': 'pw'}}
        UserTest.DummyUser.login('name', 'pw')
        UserTest.usersDAOMock.get_user_by_name.assert_called_once_with('name')

    def test_login_with_wrong_password(self):
        UserTest.usersDAOMock.get_user_by_name.return_value = {'login': {'name': 'name', 'passwordHash': 'pw'}}
        with self.assertRaises(IncorrectPasswordError):
            UserTest.DummyUser.login('name', 'wrong_pw')
        UserTest.usersDAOMock.get_user_by_name.assert_called_once_with('name')

    def test_login_with_unknown_user(self):
        UserTest.usersDAOMock.get_user_by_name.return_value = None
        with self.assertRaises(UserNotFoundError):
            UserTest.DummyUser.login('name', 'pw')
        UserTest.usersDAOMock.get_user_by_name.assert_called_once_with('name')
