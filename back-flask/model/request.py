from __future__ import annotations

from typing import List, Tuple, Optional, Dict, Any, Type

from bson import ObjectId

from dao.requests_dao import RequestsDAO
from db import db
from model.abstract_model import AbstractModel
from model.exception import UnauthorizedAccessError, UnexpectedRequestStatusError
from model.item import Item
from model.request_status import RequestStatus
from model.user import Requester, Volunteer


class Request(AbstractModel):

    def __init__(self, requester: str, status: int, items: List[Tuple[Item, int]], id: Optional[str] = None, volunteer: Optional[str] = None):
        self.requester = requester
        self.status = status
        self.items = items
        self.volunteer = volunteer
        super(Request, self).__init__(id)

    @classmethod
    def get_dao(cls) -> RequestsDAO:
        return RequestsDAO(db)

    @classmethod
    def get_item_cls(cls) -> Type[Item]:
        return Item

    @classmethod
    def resolve_items_from_ids(cls, item_amount_dicts: List[Dict[str, Any]]) -> List[Tuple[Item, int]]:
        return [
            (
                cls.get_item_cls().get_from_id(str(item['id'])),
                item['amount']
            ) for item in item_amount_dicts
        ]

    @classmethod
    def from_db_object(cls, db_object) -> Request:
        return Request(
            requester=str(db_object['requester']),
            status=db_object['status'],
            items=cls.resolve_items_from_ids(db_object['items']),
            id=str(db_object['_id']),
            volunteer=None if db_object['volunteer'] is None else str(db_object['volunteer'])
        )

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'requester': ObjectId(self.requester),
            'volunteer': None if self.volunteer is None else ObjectId(self.volunteer),
            'status': self.status,
            'items': [
                {
                    'id': ObjectId(item.id),
                    'amount': amount
                } for item, amount in self.items
            ]
        }

    def to_response(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'requester': self.requester,
            'volunteer': self.volunteer,
            'status': self.status,
            'items': [
                {
                    'item': item.to_response(),
                    'amount': amount
                } for item, amount in self.items
            ]
        }

    @classmethod
    def create_request(cls, items: List[Dict[str, Any]], session_id: str) -> str:
        request = Request(
            requester=Requester.get_user_id_from_session_id(session_id),
            status=RequestStatus.CREATED,
            items=cls.resolve_items_from_ids(items),
        )
        id = cls.get_dao().store_one(request.to_db_object())
        return id

    @classmethod
    def submit_request(cls, request_id: str, session_id: str) -> str:
        requester_id = Requester.get_user_id_from_session_id(session_id)
        request = cls.get_from_id(request_id)
        if not request.requester == requester_id:
            raise UnauthorizedAccessError
        if not request.status == RequestStatus.CREATED:
            raise UnexpectedRequestStatusError(request.status, RequestStatus.CREATED)
        cls.get_dao().update_status(request.id, RequestStatus.SUBMITTED)
        return 'Request submitted successfully'

    @classmethod
    def get_requesters_own_requests(cls, session_id: str) -> List[Dict[str, Any]]:
        requester_id = Requester.get_user_id_from_session_id(session_id)
        requests = [cls.from_db_object(db_obj) for db_obj in cls.get_dao().get_requests_by_requester(requester_id)]
        return [request.to_response() for request in requests]

    @classmethod
    def get_open_requests(cls, session_id: str) -> List[Dict[str, Any]]:
        Volunteer.get_user_id_from_session_id(session_id)
        requests = [cls.from_db_object(db_obj) for db_obj in cls.get_dao().get_open_requests()]
        return [request.to_response() for request in requests]

    @classmethod
    def get_volunteers_own_requests(cls, session_id: str) -> List[Dict[str, Any]]:
        volunteer_id = Volunteer.get_user_id_from_session_id(session_id)
        requests = [cls.from_db_object(db_obj) for db_obj in cls.get_dao().get_requests_by_volunteer(volunteer_id)]
        return [request.to_response() for request in requests]

    @classmethod
    def accept_request(cls, request_id: str, session_id: str) -> str:
        volunteer_id = Volunteer.get_user_id_from_session_id(session_id)
        request = cls.get_from_id(request_id)
        if not request.status == RequestStatus.SUBMITTED:
            raise UnexpectedRequestStatusError(request.status, RequestStatus.SUBMITTED)
        cls.get_dao().update_volunteer_and_status(request.id, volunteer_id, RequestStatus.IN_PROGRESS)
        return 'Request accepted successfully'
