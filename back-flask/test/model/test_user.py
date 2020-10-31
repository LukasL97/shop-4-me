from unittest import TestCase

from dao.users_dao import UsersDAO, RequestersDAO
from model.exception import IncorrectPasswordError, UserNotFoundError, UserAlreadyRegisteredError, \
    UserSessionIdNotFoundError, UnexpectedNumberOfLocationsForAddressError
from model.location.address import AddressHandler
from model.user import User, UserHandler, RequesterHandler, Requester
from test.model.util.stubs import AddressLocatorStub
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


class RequesterHandlerTest(TestCase):

    db = get_empty_local_test_db(['Requester'])
    dao = RequestersDAO(db)
    address_handler = AddressHandler(AddressLocatorStub())
    requester_handler = RequesterHandler(dao, address_handler)

    def setUp(self):
        self.dao.clear()
        self.requester_handler.active_user_sessions.clear()

    def test_set_address_correctly(self):
        session_id = 'someId'
        requester = Requester('login', 'pw', 'first', 'last')
        requester_id = self.dao.store_one(requester.to_db_object())
        requester.id = requester_id
        self.requester_handler.active_user_sessions[session_id] = requester
        self.requester_handler.set_address('Some Street 42', '1337', 'Funland', session_id)
        self.assertEqual(len(self.dao.get_all()), 1)
        self.assertEqual(self.dao.get_all()[0]['address']['street'], 'Some Street 42')
        self.assertEqual(self.dao.get_all()[0]['address']['zip'], '1337')
        self.assertEqual(self.dao.get_all()[0]['address']['country'], 'Funland')
        self.assertEqual(self.dao.get_all()[0]['address']['coordinates']['lat'], 42.0)
        self.assertEqual(self.dao.get_all()[0]['address']['coordinates']['lng'], 13.37)

    def test_update_address_correctly_if_already_set(self):
        session_id = 'someId'
        requester = Requester('login', 'pw', 'first', 'last')
        requester_id = self.dao.store_one(requester.to_db_object())
        requester.id = requester_id
        self.requester_handler.active_user_sessions[session_id] = requester
        self.requester_handler.set_address('Some Street 42', '1337', 'Funland', session_id)
        self.requester_handler.set_address('Other Street 24', '12345', 'Otherland', session_id)
        self.assertEqual(len(self.dao.get_all()), 1)
        self.assertEqual(self.dao.get_all()[0]['address']['street'], 'Other Street 24')
        self.assertEqual(self.dao.get_all()[0]['address']['zip'], '12345')
        self.assertEqual(self.dao.get_all()[0]['address']['country'], 'Otherland')
        self.assertEqual(self.dao.get_all()[0]['address']['coordinates']['lat'], 23.0)
        self.assertEqual(self.dao.get_all()[0]['address']['coordinates']['lng'], 32.0)

    def test_set_address_with_unknown_session_id(self):
        session_id = 'someId'
        self.assertNotIn(session_id, self.requester_handler.active_user_sessions)
        with self.assertRaises(UserSessionIdNotFoundError):
            self.requester_handler.set_address('Some Street 42', '1337', 'Funland', session_id)

    def test_set_address_with_failing_geolocation(self):
        session_id = 'someId'
        requester = Requester('login', 'pw', 'first', 'last')
        requester_id = self.dao.store_one(requester.to_db_object())
        requester.id = requester_id
        self.requester_handler.active_user_sessions[session_id] = requester
        with self.assertRaises(UnexpectedNumberOfLocationsForAddressError):
            self.requester_handler.set_address('Unknown Street 33', '12345', 'Nomansland', session_id)

