from typing import List, Dict, Any

from bson import ObjectId
from pymongo.database import Database

from dao.abstract_dao import AbstractDAO


class TimeFramesDAO(AbstractDAO):

    def __init__(self, db: Database):
        super().__init__(db, 'TimeFrames')

    def get_time_frames_by_volunteer(self, volunteer_id: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({'volunteer': ObjectId(volunteer_id)}))

    def update_requests(self, id: str, requests: List[str]) -> None:
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': {'requests': requests}})
