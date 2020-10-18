from typing import List, Dict, Any

from bson import ObjectId
from pymongo.database import Database

from dao.abstract_dao import AbstractDAO
from model.request_status import RequestStatus


class RequestsDAO(AbstractDAO):

    def __init__(self, db: Database):
        super(RequestsDAO, self).__init__(db, 'Requests')

    def get_requests_by_requester(self, requester_id: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({'requester': ObjectId(requester_id)}))

    def get_requests_by_volunteer(self, volunteer_id: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({'volunteer': ObjectId(volunteer_id)}))

    def get_open_requests(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({'status': RequestStatus.SUBMITTED}))

    def update_status(self, id: str, status: int) -> None:
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': {'status': status}})

    def update_volunteer_and_status(self, id: str, volunteer_id: str, status: int) -> None:
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': {'volunteer': ObjectId(volunteer_id), 'status': status}})
