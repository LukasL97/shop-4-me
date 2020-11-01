from flask import Response, request, make_response, jsonify

from api.http_status import OK, BAD_REQUEST, UNAUTHORIZED, NOT_FOUND
from model.exception import UserSessionIdNotFoundError, UnauthorizedAccessError, ObjectIdNotFoundError
from model.time_frame import TimeFrameHandler
from spec import DocumentedBlueprint

time_frame = DocumentedBlueprint('time_frame', __name__)


@time_frame.route('/timeframe', methods=['POST'])
def add_time_frame(time_frame_handler: TimeFrameHandler) -> Response:
    '''
    ---
    post:
        summary: create an empty timeframe as a volunteer
        description: Timeframes can be filled with requests for the volunteer to keep track of their schedule. The time format is "YYYY-MM-DD hh:mm:ss".
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            start:
                                type: string
                                description: format "YYYY-MM-DD hh:mm:ss"
                            end:
                                type: string
                                description: format "YYYY-MM-DD hh:mm:ss"
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Volunteer
        responses:
            200:
                description: id of the successfully created timeframe
                content:
                    string:
                        schema:
                            type: string
                            description: timeframe id
            400:
                description: incorrect request body or time string format
            401:
                description: could not find logged in volunteer with given sessionId
    '''
    body = request.json
    try:
        return make_response(
            time_frame_handler.add_time_frame(
                start=body['start'],
                end=body['end'],
                session_id=body['sessionId']
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Volunteer with session id %s not found' % body['sessionId'], UNAUTHORIZED)
    except ValueError as error:
        return make_response(error.args[0], BAD_REQUEST)


@time_frame.route('/timeframes', methods=['POST'])
def get_time_frames(time_frame_handler: TimeFrameHandler) -> Response:
    '''
    ---
    post:
        summary: get all own timeframes as a volunteer
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Volunteer
        responses:
            200:
                description: list of all timeframes of the querying volunteer
                content:
                    array:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: string
                                    volunteer:
                                        type: string
                                        description: id of the volunteer who owns this timeframe
                                    start:
                                        type: string
                                        description: format "YYYY-MM-DD hh:mm:ss"
                                    end:
                                        type: string
                                        description: format "YYYY-MM-DD hh:mm:ss"
                                    requests:
                                        type: array
                                        items:
                                            type: string
                                            description: id of a request scheduled in this timeframe
            400:
                description: incorrect request body
            401:
                description: could not find logged in volunteer with given sessionId
    '''
    body = request.json
    try:
        return make_response(jsonify(
            time_frame_handler.get_time_frames(body['sessionId'])
        ), OK)
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Volunteer with session id %s not found' % body['sessionId'], UNAUTHORIZED)


@time_frame.route('/timeframe/request', methods=['POST'])
def add_request_to_time_frame(time_frame_handler: TimeFrameHandler) -> Response:
    '''
    ---
    post:
        summary: schedule a request in a timeframe as a volunteer
        description: The volunteer can only schedule requests that they accepted and only schedule them in a timeframe they created.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            timeframeId:
                                type: string
                                description: id of a timeframe previously created by this volunteer
                            requestId:
                                type: string
                                description: id of a request previously accepted by this volunteer
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Volunteer
        responses:
            200:
                description: request added to timeframe successfully
            400:
                description: incorrect request body
            401:
                description: could not find logged in volunteer with given sessionId OR tried accessing timeframe or request that does not belong to this volunteer
            404:
                description: tried accessing an non-existing timeframe or request
    '''
    body = request.json
    try:
        return make_response(
            time_frame_handler.add_request_to_time_frame(
                time_frame_id=body['timeframeId'],
                request_id=body['requestId'],
                session_id=body['sessionId']
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Volunteer with session id %s not found' % body['sessionId'], UNAUTHORIZED)
    except ObjectIdNotFoundError as error:
        return make_response('Object of type %s with id %s does not exist' % (error.object_type, error.object_id), NOT_FOUND)
    except UnauthorizedAccessError:
        return make_response('Tried accessing timeframe OR request that does not belong to this volunteer', UNAUTHORIZED)
