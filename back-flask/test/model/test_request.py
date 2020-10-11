from typing import Type
from unittest import TestCase
from unittest.mock import Mock

from dao.items_dao import ItemsDAO
from dao.requests_dao import RequestsDAO
from model.exception import UserSessionIdNotFoundError, ObjectIdNotFoundError
from model.item import Item
from model.request import Request, RequestStatus
from model.user import Requester
from test.mongodb_integration_test_setup import get_empty_local_test_db


class DummyItem(Item):

    @classmethod
    def get_dao(cls) -> ItemsDAO:
        return ItemsDAO(RequestTest.db)

class DummyRequest(Request):

    @classmethod
    def get_dao(cls) -> RequestsDAO:
        return RequestsDAO(RequestTest.db)

    @classmethod
    def get_item_cls(cls) -> Type[Item]:
        return DummyItem

class RequestTest(TestCase):

    db = get_empty_local_test_db(['Requests', 'Items'])

    def setUp(self):
        DummyRequest.get_dao().clear()
        DummyItem.get_dao().clear()
        Requester.active_user_sessions.clear()

    def test_create_request_correctly(self):
        session_id = 'sessionId'
        requester = Requester('login', 'pw', 'first', 'last', '5f81ae776db502d353a84fdf')
        Requester.active_user_sessions[session_id] = requester
        item_1 = DummyItem(
            'item1',
            42.42,
            'category',
            '5f7c28c6e979c6a33a1f3f79',
        )
        item_2 = DummyItem(
            'item2',
            13.37,
            'category',
            '5f7c28c6e979c6a33a1f3f79',
        )
        item_1_id = DummyItem.get_dao().store_one(item_1.to_db_object())
        item_2_id = DummyItem.get_dao().store_one(item_2.to_db_object())
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
        request_id = DummyRequest.create_request(request_items, session_id)
        requests = DummyRequest.get_dao().get_all()
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
        Requester.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            DummyRequest.create_request([], 'otherSessionId')

    def test_create_request_with_unknown_item_id(self):
        session_id = 'sessionId'
        requester = Requester('login', 'pw', 'first', 'last', 'userId')
        Requester.active_user_sessions[session_id] = requester
        item_id = '5f7c28c6e979c6a33a1f3f79'
        with self.assertRaises(ObjectIdNotFoundError):
            DummyRequest.create_request(
                [{'id': item_id, 'amount': 3}],
                session_id
            )

    def test_get_requesters_own_requests_correctly(self):
        session_id = 'sessionId'
        requester_id = '5f7c2d96e48e242b81178822'
        other_requester_id = '5f81ae36fa3b02a743177500'
        requester = Requester('login', 'pw', 'first', 'last', requester_id)
        Requester.active_user_sessions[session_id] = requester
        item = DummyItem(
            'item',
            42.42,
            'category',
            '5f7c28c6e979c6a33a1f3f79',
        )
        item_id = DummyItem.get_dao().store_one(item.to_db_object())
        item.id = item_id
        request_1 = DummyRequest(
            requester=requester_id,
            status=RequestStatus.CREATED,
            items=[],
            volunteer=None,
        )
        request_2 = DummyRequest(
            requester=requester_id,
            status=RequestStatus.IN_PROGRESS,
            items=[(item, 3)],
            volunteer='5f81ae776db502d353a84fdf'
        )
        request_3 = DummyRequest(
            requester=other_requester_id,
            status=RequestStatus.PAID,
            items=[(item, 1)],
            volunteer='5f81ae776db502d353a84fdf'
        )
        request_1_id = DummyRequest.get_dao().store_one(request_1.to_db_object())
        request_2_id = DummyRequest.get_dao().store_one(request_2.to_db_object())
        request_3_id = DummyRequest.get_dao().store_one(request_3.to_db_object())
        requests = DummyRequest.get_requesters_own_requests(session_id)
        self.assertEqual(len(requests), 2)
        self.assertIn(request_1_id, [request['id'] for request in requests])
        self.assertIn(request_2_id, [request['id'] for request in requests])
        self.assertEqual(len([r for r in requests if r['id'] == request_2_id][0]['items']), 1)
        self.assertEqual(
            [r for r in requests if r['id'] == request_2_id][0]['items'][0]['item']['id'],
            item_id
        )

    def test_get_requesters_own_requests_with_unknown_session_id(self):
        Requester.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            DummyRequest.get_requesters_own_requests('otherSessionId')
