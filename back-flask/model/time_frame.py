from datetime import datetime
from typing import Dict, Any, List, Optional, cast

from bson import ObjectId
from injector import inject

from dao.time_frames_dao import TimeFramesDAO
from model.abstract_model import AbstractModel, AbstractHandler
from model.exception import ObjectIdNotFoundError, UnauthorizedAccessError
from model.request import RequestHandler, Request
from model.user import VolunteerHandler


class TimeFrame(AbstractModel):

    def __init__(self, volunteer: str, start: datetime, end: datetime, requests: List[str], id: Optional[str] = None):
        self.volunteer: str = volunteer
        self.start: datetime = start
        self.end: datetime = end
        self.requests: List[str] = requests
        super().__init__(id)

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'volunteer': ObjectId(self.volunteer),
            'start': self.start,
            'end': self.end,
            'requests': [ObjectId(request) for request in self.requests]
        }

    def to_response(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'volunteer': self.volunteer,
            'start': str(self.start),
            'end': str(self.end),
            'requests': self.requests
        }


class TimeFrameHandler(AbstractHandler):

    @inject
    def __init__(self, dao: TimeFramesDAO, volunteer_handler: VolunteerHandler, request_handler: RequestHandler):
        self.dao: TimeFramesDAO = dao
        self.volunteer_handler: VolunteerHandler = volunteer_handler
        self.request_handler: RequestHandler = request_handler
        super().__init__(TimeFrame, dao)

    def from_db_object(self, db_object: Dict[str, Any]) -> TimeFrame:
        return TimeFrame(
            volunteer=str(db_object['volunteer']),
            start=db_object['start'],
            end=db_object['end'],
            requests=db_object['requests'],
            id=str(db_object['_id'])
        )

    def add_time_frame(self, start: str, end: str, session_id: str) -> str:
        volunteer_id = self.volunteer_handler.get_user_id_from_session_id(session_id)
        start = datetime.fromisoformat(start)
        end = datetime.fromisoformat(end)
        time_frame = TimeFrame(
            volunteer=volunteer_id,
            start=start,
            end=end,
            requests=[],
        )
        id = self.dao.store_one(time_frame.to_db_object())
        return id

    def get_time_frames(self, session_id: str) -> List[Dict[str, Any]]:
        volunteer_id = self.volunteer_handler.get_user_id_from_session_id(session_id)
        time_frames = [self.from_db_object(db_obj) for db_obj in self.dao.get_time_frames_by_volunteer(volunteer_id)]
        return [time_frame.to_response() for time_frame in time_frames]

    def add_request_to_time_frame(self, time_frame_id: str, request_id: str, session_id: str) -> str:
        volunteer_id = self.volunteer_handler.get_user_id_from_session_id(session_id)
        time_frame = cast(TimeFrame, self.get_from_id(time_frame_id))
        if not time_frame.volunteer == volunteer_id:
            raise UnauthorizedAccessError
        request = cast(Request, self.request_handler.get_from_id(request_id))
        if not request.volunteer == volunteer_id:
            raise UnauthorizedAccessError
        time_frame.requests.append(request_id)
        self.dao.update_requests(time_frame.id, time_frame.requests)
        return 'Request successfully added'
