from datetime import datetime
from unittest import TestCase

from bson import ObjectId

from dao.requests_dao import RequestsDAO
from dao.time_frames_dao import TimeFramesDAO
from model.exception import UserSessionIdNotFoundError, UnauthorizedAccessError, ObjectIdNotFoundError
from model.request import RequestHandler, Request
from model.request_status import RequestStatus
from model.time_frame import TimeFrameHandler, TimeFrame
from model.user import VolunteerHandler, Volunteer
from test.mongodb_integration_test_setup import get_empty_local_test_db


class TimeFrameHandlerTest(TestCase):

    db = get_empty_local_test_db(['TimeFrames', 'Requests'])
    dao = TimeFramesDAO(db)
    volunteer_handler = VolunteerHandler(None)
    requests_dao = RequestsDAO(db)
    request_handler = RequestHandler(requests_dao, None, None, None, None)
    time_frame_handler = TimeFrameHandler(dao, volunteer_handler, request_handler)

    def setUp(self) -> None:
        self.dao.clear()
        self.requests_dao.clear()
        self.volunteer_handler.active_user_sessions.clear()

    def test_add_time_frame_correctly(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        start = '2020-10-25 12:00:00'
        end = '2020-10-25 14:00:00'
        id = self.time_frame_handler.add_time_frame(start, end, session_id)
        time_frames = self.dao.get_time_frames_by_volunteer(volunteer_id)
        self.assertEqual(len(time_frames), 1)
        self.assertEqual(str(time_frames[0]['_id']), id)
        self.assertEqual(str(time_frames[0]['volunteer']), volunteer_id)
        self.assertEqual(str(time_frames[0]['start']), start)
        self.assertEqual(str(time_frames[0]['end']), end)
        self.assertEqual(time_frames[0]['requests'], [])

    def test_add_time_frame_with_unknown_session_id(self):
        self.assertEqual(len(self.volunteer_handler.active_user_sessions), 0)
        with self.assertRaises(UserSessionIdNotFoundError):
            self.time_frame_handler.add_time_frame('2020-10-25 12:00:00', '2020-10-25 14:00:00', 'sessionId')

    def test_add_time_frame_incorrect_date_pattern(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        incorrect_date_pattern = '20201025,12,00,00'
        with self.assertRaises(ValueError):
            self.time_frame_handler.add_time_frame(incorrect_date_pattern, '2020-10-25 14:00:00', session_id)

    def test_get_time_frames_correctly(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        other_volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        time_frame_1 = TimeFrame(volunteer_id, datetime.fromisoformat('2020-10-25 12:00:00'), datetime.fromisoformat('2020-10-25 14:00:00'), [])
        time_frame_2 = TimeFrame(other_volunteer_id, datetime.fromisoformat('2020-10-25 12:00:00'), datetime.fromisoformat('2020-10-25 14:00:00'), [])
        time_frame_1_id = self.dao.store_one(time_frame_1.to_db_object())
        time_frame_2_id = self.dao.store_one(time_frame_2.to_db_object())
        time_frames = self.time_frame_handler.get_time_frames(session_id)
        self.assertEqual(len(time_frames), 1)
        self.assertEqual(time_frames[0]['id'], time_frame_1_id)

    def test_get_time_frames_with_unknown_session_id(self):
        self.assertEqual(len(self.volunteer_handler.active_user_sessions), 0)
        with self.assertRaises(UserSessionIdNotFoundError):
            self.time_frame_handler.get_time_frames('sessionId')

    def test_add_request_to_time_frame_correctly(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        time_frame = TimeFrame(volunteer_id, datetime.fromisoformat('2020-10-25 12:00:00'), datetime.fromisoformat('2020-10-25 14:00:00'), [])
        time_frame.id = self.dao.store_one(time_frame.to_db_object())
        request_1 = Request(
            requester=str(ObjectId()),
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=volunteer_id
        )
        request_2 = Request(
            requester=str(ObjectId()),
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=volunteer_id
        )
        request_1.id = self.requests_dao.store_one(request_1.to_db_object())
        request_2.id = self.requests_dao.store_one(request_2.to_db_object())
        self.time_frame_handler.add_request_to_time_frame(time_frame.id, request_1.id, session_id)
        self.time_frame_handler.add_request_to_time_frame(time_frame.id, request_2.id, session_id)
        time_frames = self.dao.get_time_frames_by_volunteer(volunteer_id)
        self.assertEqual(len(time_frames), 1)
        self.assertEqual(str(time_frames[0]['_id']), time_frame.id)
        self.assertEqual(len(time_frames[0]['requests']), 2)
        self.assertEqual(str(time_frames[0]['requests'][0]), request_1.id)
        self.assertEqual(str(time_frames[0]['requests'][1]), request_2.id)

    def test_add_request_to_time_frame_with_unknown_session_id(self):
        self.assertEqual(len(self.volunteer_handler.active_user_sessions), 0)
        with self.assertRaises(UserSessionIdNotFoundError):
            self.time_frame_handler.add_request_to_time_frame(str(ObjectId()), str(ObjectId()), 'sessionId')

    def test_add_request_to_time_frame_with_incorrect_time_frame_id(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        request = Request(
            requester=str(ObjectId()),
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=volunteer_id
        )
        request.id = self.requests_dao.store_one(request.to_db_object())
        self.assertEqual(len(self.dao.get_all()), 0)
        with self.assertRaises(ObjectIdNotFoundError):
            self.time_frame_handler.add_request_to_time_frame(str(ObjectId()), request.id, session_id)

    def test_add_request_to_time_frame_with_incorrect_request_id(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        time_frame = TimeFrame(volunteer_id, datetime.fromisoformat('2020-10-25 12:00:00'), datetime.fromisoformat('2020-10-25 14:00:00'), [])
        time_frame.id = self.dao.store_one(time_frame.to_db_object())
        self.assertEqual(len(self.requests_dao.get_all()), 0)
        with self.assertRaises(ObjectIdNotFoundError):
            self.time_frame_handler.add_request_to_time_frame(time_frame.id, str(ObjectId()), session_id)

    def test_add_request_to_time_frame_with_incorrect_volunteer_id_at_time_frame(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        other_volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        time_frame = TimeFrame(other_volunteer_id, datetime.fromisoformat('2020-10-25 12:00:00'), datetime.fromisoformat('2020-10-25 14:00:00'), [])
        time_frame.id = self.dao.store_one(time_frame.to_db_object())
        request = Request(
            requester=str(ObjectId()),
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=volunteer_id
        )
        request.id = self.requests_dao.store_one(request.to_db_object())
        with self.assertRaises(UnauthorizedAccessError):
            self.time_frame_handler.add_request_to_time_frame(time_frame.id, request.id, session_id)

    def test_add_request_to_time_frame_with_incorrect_volunteer_id_at_request(self):
        session_id = 'someId'
        volunteer_id = str(ObjectId())
        other_volunteer_id = str(ObjectId())
        volunteer = Volunteer('login', 'pw', 'first', 'last', volunteer_id)
        self.volunteer_handler.active_user_sessions[session_id] = volunteer
        time_frame = TimeFrame(volunteer_id, datetime.fromisoformat('2020-10-25 12:00:00'), datetime.fromisoformat('2020-10-25 14:00:00'), [])
        time_frame.id = self.dao.store_one(time_frame.to_db_object())
        request = Request(
            requester=str(ObjectId()),
            status=RequestStatus.IN_PROGRESS,
            items=[],
            volunteer=other_volunteer_id
        )
        request.id = self.requests_dao.store_one(request.to_db_object())
        with self.assertRaises(UnauthorizedAccessError):
            self.time_frame_handler.add_request_to_time_frame(time_frame.id, request.id, session_id)


