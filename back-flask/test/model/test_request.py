from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dao.items_dao import ItemsDAO
from dao.requests_dao import RequestsDAO
from model.exception import UserSessionIdNotFoundError, ObjectIdNotFoundError, UnauthorizedAccessError, \
    UnexpectedRequestStatusError, MissingDeliveryAddressError
from model.image import Image
from model.item import Item, ItemHandler
from model.location.address import AddressHandler, Address
from model.product_details import ProductDetails
from model.request import RequestHandler, Request
from model.request_status import RequestStatus
from model.shop import ShopHandler
from model.user import Requester, Volunteer, ShopOwnerHandler, RequesterHandler, VolunteerHandler
from test.model.util.stubs import AddressLocatorStub
from test.mongodb_integration_test_setup import get_empty_local_test_db


class RequestHandlerTest(TestCase):

    db = get_empty_local_test_db(['Requests', 'Items', 'Shops'])
    requests_dao = RequestsDAO(db)
    items_dao = ItemsDAO(db)
    item_handler = ItemHandler(items_dao, ShopOwnerHandler(None), None)
    requester_handler = RequesterHandler(None, None)
    volunteer_handler = VolunteerHandler(None)
    locator = AddressLocatorStub()
    address_handler = AddressHandler(locator)
    request_handler = RequestHandler(requests_dao, item_handler, requester_handler, volunteer_handler, address_handler)

    def setUp(self):
        self.requests_dao.clear()
        self.items_dao.clear()
        self.requester_handler.active_user_sessions.clear()
        self.volunteer_handler.active_user_sessions.clear()

    def test_create_request_correctly(self):
        session_id = 'sessionId'
        requester = Requester('login', 'pw', 'first', 'last', '5f81ae776db502d353a84fdf')
        self.requester_handler.active_user_sessions[session_id] = requester
        item_1 = Item(
            'item1',
            42.42,
            'category',
            '5f7c28c6e979c6a33a1f3f79',
            ProductDetails('', {}),
            Image('', '')
        )
        item_2 = Item(
            'item2',
            13.37,
            'category',
            '5f7c28c6e979c6a33a1f3f79',
            ProductDetails('', {}),
            Image('', '')
        )
        item_1_id = self.items_dao.store_one(item_1.to_db_object())
        item_2_id = self.items_dao.store_one(item_2.to_db_object())
        item_1_amount = 5
        item_2_amount = 3
        request_items = [
            {
                'id': item_1_id,
                'amount': item_1_amount
            },
            {
                'id': item_2_id,
                'amount': item_2_amount
            }
        ]
        request_id = self.request_handler.create_request(request_items, session_id)
        requests = self.requests_dao.get_all()
        self.assertEqual(len(requests), 1)
        self.assertEqual(str(requests[0]['_id']), request_id)
        self.assertEqual(str(requests[0]['requester']), requester.id)
        self.assertEqual(requests[0]['volunteer'], None)
        self.assertEqual(requests[0]['status'], RequestStatus.CREATED)
        self.assertEqual(str(requests[0]['items'][0]['id']), item_1_id)
        self.assertEqual(requests[0]['items'][0]['amount'], item_1_amount)
        self.assertEqual(str(requests[0]['items'][1]['id']), item_2_id)
        self.assertEqual(requests[0]['items'][1]['amount'], item_2_amount)

    def test_create_request_with_unknown_session_id(self):
        self.requester_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.request_handler.create_request([], 'otherSessionId')

    def test_create_request_with_unknown_item_id(self):
        session_id = 'sessionId'
        requester = Requester('login', 'pw', 'first', 'last', 'userId')
        self.requester_handler.active_user_sessions[session_id] = requester
        item_id = '5f7c28c6e979c6a33a1f3f79'
        with self.assertRaises(ObjectIdNotFoundError):
            self.request_handler.create_request(
                [{'id': item_id, 'amount': 3}],
                session_id
            )

    def test_submit_request_without_address_correctly(self):
        session_id = 'sessionId'
        requester_id = '5f81ae776db502d353a84fdf'
        address = self.address_handler(self.locator.valid_street_1, self.locator.valid_zip_1, self.locator.valid_country_1)
        requester = Requester('login', 'pw', 'first', 'last', requester_id, address)
        self.requester_handler.active_user_sessions[session_id] = requester
        request = Request(
            requester=requester_id,
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None
        )
        request_id = self.requests_dao.store_one(request.to_db_object())
        self.request_handler.submit_request(request_id, session_id)
        request = self.request_handler.from_db_object(self.requests_dao.get_all()[0])
        self.assertEqual(request.status, RequestStatus.SUBMITTED)
        self.assertEqual(request.delivery_address, address)
        self.assertIsNot(request.submission_date, None)
        self.assertTrue(type(request.submission_date) == datetime)

    def test_submit_request_with_address_correctly(self):
        session_id = 'sessionId'
        requester_id = '5f81ae776db502d353a84fdf'
        address = self.address_handler(self.locator.valid_street_1, self.locator.valid_zip_1, self.locator.valid_country_1)
        requester = Requester('login', 'pw', 'first', 'last', requester_id)
        self.requester_handler.active_user_sessions[session_id] = requester
        request = Request(
            requester=requester_id,
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None,
        )
        request_id = self.requests_dao.store_one(request.to_db_object())
        self.request_handler.submit_request(request_id, session_id, address.to_db_object())
        request = self.request_handler.from_db_object(self.requests_dao.get_all()[0])
        self.assertEqual(request.status, RequestStatus.SUBMITTED)
        self.assertEqual(request.delivery_address, address)
        self.assertIsNot(request.submission_date, None)
        self.assertTrue(type(request.submission_date) == datetime)

    def test_submit_request_with_unknown_session_id(self):
        self.requester_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.request_handler.submit_request('requestId', 'otherSessionId')

    def test_submit_request_with_unknown_object_id(self):
        session_id = 'sessionId'
        requester = Requester('login', 'pw', 'first', 'last', '5f81ae776db502d353a84fdf')
        self.requester_handler.active_user_sessions[session_id] = requester
        self.assertEqual(len(self.requests_dao.get_all()), 0)
        request_id = '5f7c28c6e979c6a33a1f3f79'
        with self.assertRaises(ObjectIdNotFoundError):
            self.request_handler.submit_request(request_id, session_id)
        self.assertEqual(len(self.requests_dao.get_all()), 0)

    def test_submit_request_of_other_requester(self):
        session_id = 'sessionId'
        requester_id = '5f81ae776db502d353a84fdf'
        other_requester_id = '5f7c28c6e979c6a33a1f3f79'
        requester = Requester('login', 'pw', 'first', 'last', requester_id)
        self.requester_handler.active_user_sessions[session_id] = requester
        request = Request(
            requester=other_requester_id,
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None
        )
        request_id = self.requests_dao.store_one(request.to_db_object())
        with self.assertRaises(UnauthorizedAccessError):
            self.request_handler.submit_request(request_id, session_id)
        self.assertEqual(self.request_handler.from_db_object(self.requests_dao.get_all()[0]).status, RequestStatus.CREATED)

    def test_submit_request_with_other_status_than_created(self):
        session_id = 'sessionId'
        requester_id = '5f81ae776db502d353a84fdf'
        requester = Requester('login', 'pw', 'first', 'last', requester_id)
        self.requester_handler.active_user_sessions[session_id] = requester
        request = Request(
            requester=requester_id,
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=None,
            submission_date=datetime.now()
        )
        request_id = self.requests_dao.store_one(request.to_db_object())
        with self.assertRaises(UnexpectedRequestStatusError):
            self.request_handler.submit_request(request_id, session_id)

    def test_submit_request_with_missing_delivery_address(self):
        session_id = 'sessionId'
        requester_id = '5f81ae776db502d353a84fdf'
        requester = Requester('login', 'pw', 'first', 'last', requester_id)
        self.requester_handler.active_user_sessions[session_id] = requester
        request = Request(
            requester=requester_id,
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None
        )
        request_id = self.requests_dao.store_one(request.to_db_object())
        with self.assertRaises(MissingDeliveryAddressError):
            self.request_handler.submit_request(request_id, session_id)

    def test_get_requesters_own_requests_correctly(self):
        session_id = 'sessionId'
        requester_id = '5f7c2d96e48e242b81178822'
        other_requester_id = '5f81ae36fa3b02a743177500'
        requester = Requester('login', 'pw', 'first', 'last', requester_id)
        self.requester_handler.active_user_sessions[session_id] = requester
        item = Item(
            'item',
            42.42,
            'category',
            '5f7c28c6e979c6a33a1f3f79',
            ProductDetails('', {}),
            Image('', '')
        )
        item_id = self.items_dao.store_one(item.to_db_object())
        item.id = item_id
        request_1 = Request(
            requester=requester_id,
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None
        )
        request_2 = Request(
            requester=requester_id,
            status=RequestStatus.IN_PROGRESS,
            items=[(item, 3)],
            volunteer='5f81ae776db502d353a84fdf',
            submission_date=datetime.now()
        )
        request_3 = Request(
            requester=other_requester_id,
            status=RequestStatus.PAID,
            items=[(item, 1)],
            volunteer='5f81ae776db502d353a84fdf',
            submission_date=datetime.now()
        )
        request_1_id = self.requests_dao.store_one(request_1.to_db_object())
        request_2_id = self.requests_dao.store_one(request_2.to_db_object())
        request_3_id = self.requests_dao.store_one(request_3.to_db_object())
        requests = self.request_handler.get_requesters_own_requests(session_id)
        self.assertEqual(len(requests), 2)
        self.assertIn(request_1_id, [request['id'] for request in requests])
        self.assertIn(request_2_id, [request['id'] for request in requests])
        self.assertEqual(len([r for r in requests if r['id'] == request_2_id][0]['items']), 1)
        self.assertEqual(
            [r for r in requests if r['id'] == request_2_id][0]['items'][0]['item']['id'],
            item_id
        )

    def test_get_requesters_own_requests_with_unknown_session_id(self):
        self.requester_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.request_handler.get_requesters_own_requests('otherSessionId')

    def test_get_open_requests_correctly(self):
        session_id = 'sessionId'
        volunteer = Volunteer('login', 'pw', 'first', 'last', 'userId')
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        request_1 = Request(
            requester='5f7c2d96e48e242b81178822',
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None,
            submission_date=datetime.now()
        )
        request_2 = Request(
            requester='5f7c2d96e48e242b81178822',
            status=RequestStatus.SUBMITTED,
            items=[],
            volunteer=None,
            submission_date=datetime.now()
        )
        request_1_id = self.requests_dao.store_one(request_1.to_db_object())
        request_2_id = self.requests_dao.store_one(request_2.to_db_object())
        requests = self.request_handler.get_open_requests(session_id)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]['id'], request_2_id)

    def test_get_open_requests_with_area_correctly(self):
        volunteer_point = (60.195382, 24.938703)
        closest_request_point = (60.195318, 24.940731)
        second_closest_request_point = (60.193371, 24.943177)
        out_of_range_request_point = (60.143397, 24.985745)
        range = 1
        session_id = 'sessionId'
        volunteer = Volunteer('login', 'pw', 'first', 'last', 'userId')
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        out_of_range_request_date = datetime.fromisoformat('2020-10-25 13:03:55.792200')
        second_closest_request_date = datetime.fromisoformat('2020-10-26 13:03:55.792200')
        closest_request_date = datetime.fromisoformat('2020-10-27 13:03:55.792200')
        closest_request = Request(
            requester='5f7c2d96e48e242b81178822',
            status=RequestStatus.SUBMITTED,
            items=[],
            volunteer=None,
            delivery_address=Address('', '', '', closest_request_point[0], closest_request_point[1]),
            submission_date=closest_request_date
        )
        second_closest_request = Request(
            requester='5f7c2d96e48e242b81178822',
            status=RequestStatus.SUBMITTED,
            items=[],
            volunteer=None,
            delivery_address=Address('', '', '', second_closest_request_point[0], second_closest_request_point[1]),
            submission_date=second_closest_request_date
        )
        out_of_range_request = Request(
            requester='5f7c2d96e48e242b81178822',
            status=RequestStatus.SUBMITTED,
            items=[],
            volunteer=None,
            delivery_address=Address('', '', '', out_of_range_request_point[0], out_of_range_request_point[1]),
            submission_date=out_of_range_request_date
        )
        closest_request_id = self.requests_dao.store_one(closest_request.to_db_object())
        second_closest_request_id = self.requests_dao.store_one(second_closest_request.to_db_object())
        out_of_range_request_id = self.requests_dao.store_one(out_of_range_request.to_db_object())
        area = {'range': range, 'lat': volunteer_point[0], 'lng': volunteer_point[1]}
        requests = self.request_handler.get_open_requests(session_id, area)
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]['id'], second_closest_request_id)
        self.assertEqual(requests[1]['id'], closest_request_id)

    def test_get_open_requests_with_unknown_session_id(self):
        self.volunteer_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.request_handler.get_open_requests('otherSessionId')

    def test_get_volunteers_own_requests_correctly(self):
        session_id = 'sessionId'
        volunteer_id = '5f7c2d96e48e242b81178822'
        other_volunteer_id = '5f81ae36fa3b02a743177500'
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        request_1 = Request(
            requester='5f81ae776db502d353a84fdf',
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None
        )
        request_2 = Request(
            requester='5f81ae776db502d353a84fdf',
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=volunteer_id,
            submission_date=datetime.now()
        )
        request_3 = Request(
            requester='5f81ae776db502d353a84fdf',
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=other_volunteer_id,
            submission_date=datetime.now()
        )
        request_1_id = self.requests_dao.store_one(request_1.to_db_object())
        request_2_id = self.requests_dao.store_one(request_2.to_db_object())
        request_3_id = self.requests_dao.store_one(request_3.to_db_object())
        requests = self.request_handler.get_volunteers_own_requests(session_id)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]['id'], request_2_id)

    def test_get_volunteers_own_requests_with_unknown_session_id(self):
        self.volunteer_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.request_handler.get_volunteers_own_requests('otherSessionId')

    def test_accept_request_correctly(self):
        session_id = 'sessionId'
        volunteer_id = '5f7c2d96e48e242b81178822'
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        request = Request(
            requester='5f81ae776db502d353a84fdf',
            status=RequestStatus.SUBMITTED,
            items=[],
            volunteer=None
        )
        request_id = self.requests_dao.store_one(request.to_db_object())
        self.request_handler.accept_request(request_id, session_id)
        request = self.request_handler.from_db_object(self.requests_dao.get_all()[0])
        self.assertEqual(request.status, RequestStatus.IN_PROGRESS)
        self.assertEqual(request.volunteer, volunteer_id)

    def test_accept_request_with_unknown_session_id(self):
        self.volunteer_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.request_handler.accept_request('5f81ae776db502d353a84fdf', 'otherSessionId')

    def test_accept_request_with_unknown_object_id(self):
        session_id = 'sessionId'
        volunteer = Volunteer('login', 'pw', 'first', 'last', '5f81ae776db502d353a84fdf')
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        self.assertEqual(len(self.requests_dao.get_all()), 0)
        request_id = '5f7c28c6e979c6a33a1f3f79'
        with self.assertRaises(ObjectIdNotFoundError):
            self.request_handler.accept_request(request_id, session_id)
        self.assertEqual(len(self.requests_dao.get_all()), 0)

    def test_accept_request_with_other_status_than_submitted(self):
        session_id = 'sessionId'
        volunteer = Volunteer('login', 'pw', 'first', 'last', '5f81ae776db502d353a84fdf')
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        request = Request(
            requester='5f7c2d96e48e242b81178822',
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None
        )
        request_id = self.requests_dao.store_one(request.to_db_object())
        with self.assertRaises(UnexpectedRequestStatusError):
            self.request_handler.accept_request(request_id, session_id)
