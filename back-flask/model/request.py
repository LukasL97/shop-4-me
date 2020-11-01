from __future__ import annotations

from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any, cast

from bson import ObjectId
from injector import inject

from dao.requests_dao import RequestsDAO
from model.abstract_model import AbstractModel, AbstractHandler
from model.exception import UnauthorizedAccessError, UnexpectedRequestStatusError, MissingDeliveryAddressError
from model.item import Item, ItemHandler
from model.location.address import Address, AddressHandler
from model.request_status import RequestStatus
from model.user import VolunteerHandler, RequesterHandler


class Request(AbstractModel):

    def __init__(self,
                 requester: str,
                 status: int,
                 items: List[Tuple[Item, int]],
                 id: Optional[str] = None,
                 volunteer: Optional[str] = None,
                 delivery_address: Optional[Address] = None,
                 submission_date: Optional[datetime] = None):
        self.requester: str = requester
        self.status: int = status
        self.items: List[Tuple[Item, int]] = items
        self.volunteer: Optional[str] = volunteer
        self.delivery_address: Optional[Address] = delivery_address
        self.submission_date: datetime = submission_date
        super(Request, self).__init__(id)

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
            ],
            'deliveryAddress': None if self.delivery_address is None else self.delivery_address.to_db_object(),
            'submissionDate': self.submission_date
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
            ],
            'deliveryAddress': None if self.delivery_address is None else self.delivery_address.to_response(),
            'submissionDate': str(self.submission_date)
        }


class RequestHandler(AbstractHandler):

    @inject
    def __init__(self,
                 dao: RequestsDAO,
                 item_handler: ItemHandler,
                 requester_handler: RequesterHandler,
                 volunteer_handler: VolunteerHandler,
                 address_handler: AddressHandler):
        self.dao: RequestsDAO = dao
        self.item_handler: ItemHandler = item_handler
        self.requester_handler: RequesterHandler = requester_handler
        self.volunteer_handler: VolunteerHandler = volunteer_handler
        self.address_handler: AddressHandler = address_handler
        super().__init__(Request, dao)

    def resolve_items_from_ids(self, item_amount_dicts: List[Dict[str, Any]]) -> List[Tuple[Item, int]]:
        return [
            (
                cast(Item, self.item_handler.get_from_id(str(item['id']))),
                item['amount']
            ) for item in item_amount_dicts
        ]

    def from_db_object(self, db_object: Dict[str, Any]) -> Request:
        return Request(
            requester=str(db_object['requester']),
            status=db_object['status'],
            items=self.resolve_items_from_ids(db_object['items']),
            id=str(db_object['_id']),
            volunteer=None if db_object['volunteer'] is None else str(db_object['volunteer']),
            delivery_address=None if db_object['deliveryAddress'] is None else self.address_handler.from_db_object(db_object['deliveryAddress']),
            submission_date=db_object['submissionDate']
        )

    def create_request(self, items: List[Dict[str, Any]], session_id: str) -> str:
        request = Request(
            requester=self.requester_handler.get_user_id_from_session_id(session_id),
            status=RequestStatus.CREATED,
            items=self.resolve_items_from_ids(items),
        )
        id = self.dao.store_one(request.to_db_object())
        return id

    def submit_request(self, request_id: str, session_id: str, delivery_address: Optional[Dict[str, str]] = None) -> str:
        requester_id = self.requester_handler.get_user_id_from_session_id(session_id)
        request = cast(Request, self.get_from_id(request_id))
        if not request.requester == requester_id:
            raise UnauthorizedAccessError
        if not request.status == RequestStatus.CREATED:
            raise UnexpectedRequestStatusError(request.status, RequestStatus.CREATED)
        requester_address = self.requester_handler.active_user_sessions[session_id].address
        if requester_address is None and delivery_address is None:
            raise MissingDeliveryAddressError
        if delivery_address is not None:
            request.delivery_address = self.address_handler(
                street=delivery_address['street'],
                zip=delivery_address['zip'],
                country=delivery_address['country']
            )
        else:
            request.delivery_address = requester_address
        self.dao.update_delivery_address(request.id, request.delivery_address.to_db_object())
        self.dao.update_submission_date(request.id, datetime.now())
        self.dao.update_status(request.id, RequestStatus.SUBMITTED)
        return 'Request submitted successfully'

    def get_requesters_own_requests(self, session_id: str) -> List[Dict[str, Any]]:
        requester_id = self.requester_handler.get_user_id_from_session_id(session_id)
        requests = [self.from_db_object(db_obj) for db_obj in self.dao.get_requests_by_requester(requester_id)]
        return [request.to_response() for request in requests]

    def get_open_requests(self, session_id: str, area: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        self.volunteer_handler.get_user_id_from_session_id(session_id)
        requests = [self.from_db_object(db_obj) for db_obj in self.dao.get_open_requests()]
        if area is not None:
            range = area['range']
            lat = area['lat']
            lng = area['lng']
            requests = [request for request in requests if request.delivery_address.distance_to_coordinates(lat, lng) <= range]
        requests.sort(key=lambda request: request.submission_date)
        return [request.to_response() for request in requests]

    def get_volunteers_own_requests(self, session_id: str) -> List[Dict[str, Any]]:
        volunteer_id = self.volunteer_handler.get_user_id_from_session_id(session_id)
        requests = [self.from_db_object(db_obj) for db_obj in self.dao.get_requests_by_volunteer(volunteer_id)]
        return [request.to_response() for request in requests]

    def accept_request(self, request_id: str, session_id: str) -> str:
        volunteer_id = self.volunteer_handler.get_user_id_from_session_id(session_id)
        request = cast(Request, self.get_from_id(request_id))
        if not request.status == RequestStatus.SUBMITTED:
            raise UnexpectedRequestStatusError(request.status, RequestStatus.SUBMITTED)
        self.dao.update_volunteer_and_status(request.id, volunteer_id, RequestStatus.IN_PROGRESS)
        return 'Request accepted successfully'
