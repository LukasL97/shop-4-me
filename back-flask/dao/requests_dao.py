from typing import List, Dict, Any

from bson import ObjectId
from pymongo.database import Database

from dao.abstract_dao import AbstractDAO


class RequestsDAO(AbstractDAO):

    def __init__(self, db: Database):
        super(RequestsDAO, self).__init__(db, 'Requests')

    def get_requests_by_requester(self, requester_id: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({'requester': ObjectId(requester_id)}))
