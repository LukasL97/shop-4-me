import flask
from flask import Response, make_response, jsonify

from api.http_status import OK, BAD_REQUEST, UNAUTHORIZED, UNPROCESSABLE_ENTITY, NOT_FOUND
from model.exception import UserSessionIdNotFoundError, ObjectIdNotFoundError, UnauthorizedAccessError, \
    UnexpectedRequestStatusError, UnexpectedUserTypeError
from model.request import RequestHandler
from spec import DocumentedBlueprint

request = DocumentedBlueprint('request', __name__)


@request.route('/request', methods=['POST'])
def create_request(request_handler: RequestHandler) -> Response:
    '''
    ---
    post:
        summary: create a request as a requester
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            items:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        id:
                                            type: string
                                            description: id of an existing item
                                        amount:
                                            type: number
                                            description: amount of this item in the request
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Requester
        responses:
            200:
                description: id of the successfully created request
                content:
                    string:
                        schema:
                            type: string
                            description: request id
            400:
                description: incorrect request body
            401:
                description: could not find logged in Requester with given sessionId
            422:
                description: request contained an unknown item id
    '''
    body = flask.globals.request.json
    try:
        return make_response(
            request_handler.create_request(
                items=body['items'],
                session_id=body['sessionId']
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Requester with session id %s not found' % body['sessionId'], UNAUTHORIZED)
    except ObjectIdNotFoundError as error:
        return make_response('Tried creating request with non-exisiting item with id %s' % error.object_id, UNPROCESSABLE_ENTITY)


@request.route('/request/submit', methods=['PATCH'])
def submit_request(request_handler: RequestHandler) -> Response:
    '''
    ---
    patch:
        summary: submit a created request as a requester
        description: Only previously created requests can be submitted. A requester may only submit requests created by themself.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            request:
                                type: string
                                description: id of the request to be submitted
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Requester
        responses:
            200:
                description: submission successful
            400:
                description: incorrect request body
            401:
                description: session id did not refer to any logged in Requester or attempt to submit request created by another Requester
            404:
                description: unknown request id
            422:
                description: attempt to submit a request that did not have status 'CREATED'
    '''
    body = flask.globals.request.json
    try:
        return make_response(
            request_handler.submit_request(
                request_id=body['request'],
                session_id=body['sessionId']
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Requester with session id %s not found' % body['sessionId'], UNAUTHORIZED)
    except ObjectIdNotFoundError as error:
        return make_response('Tried submitting request with unknown request id %s' % error.object_id, NOT_FOUND)
    except UnauthorizedAccessError:
        return make_response('Tried submitting request that has been created by another requester', UNAUTHORIZED)
    except UnexpectedRequestStatusError as error:
        return make_response('Tried submitting request that did not have expected status %d, but status %d' % (error.expected, error.actual), UNPROCESSABLE_ENTITY)


@request.route('/request/accept', methods=['PATCH'])
def accept_request(request_handler: RequestHandler) -> Response:
    '''
    ---
    patch:
        summary: accept a submitted request as a volunteer
        description: Only previously submitted requests can be accepted.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            request:
                                type: string
                                description: id of the request to be accepted
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Volunteer
        responses:
            200:
                description: request accepted successfully
            400:
                description: incorrect request body
            401:
                description: session id did not refer to any logged in Volunteer
            404:
                description: unknown request id
            422:
                description: attempt to accept a request that did not have status 'SUBMITTED'
    '''
    body = flask.globals.request.json
    try:
        return make_response(
            request_handler.accept_request(
                request_id=body['request'],
                session_id=body['sessionId']
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Volunteer with session id %s not found' % body['sessionId'], UNAUTHORIZED)
    except ObjectIdNotFoundError as error:
        return make_response('Tried accepting request with unknown request id %s' % error.object_id, NOT_FOUND)
    except UnexpectedRequestStatusError as error:
        return make_response('Tried accepting request that did not have expected status %d, but status %d' % (error.expected, error.actual), UNPROCESSABLE_ENTITY)


@request.route('/requests/open', methods=['GET'])
def get_open_requests(request_handler: RequestHandler) -> Response:
    '''
    ---
    get:
        summary: get a list of open requests as a Volunteer
        description: Open requests are requests that have been created and submitted by a Requester, but not yet accepted by any Volunteer.
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
                description: list of all open requests with items directly inlined
                content:
                    array:
                        schema:
                            type: array
                            items:
                                <REQUEST>
            400:
                description: incorrect request body
            401:
                description: could not find logged in Volunteer with given sessionId
    '''
    body = flask.globals.request.json
    try:
        return make_response(jsonify(request_handler.get_open_requests(body['sessionId'])), OK)
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Volunteer with session id %s not found' % body['sessionId'], UNAUTHORIZED)


@request.route('/requests/own', methods=['GET'])
def get_own_requests(request_handler: RequestHandler) -> Response:
    '''
    ---
    get:
        summary: get a list of your own requests as a Requester or Volunteer
        description: If Requester, get a list of requests created by yourself. If Volunteer, get a list of requests accepted by yourself.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            userType:
                                type: string
                                description: either "Requester" or "Volunteer"
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Requester/Volunteer
        responses:
            200:
                description: list of all requests of this Requester/Volunteer with items directly inlined
                content:
                    array:
                        schema:
                            type: array
                            items:
                                <REQUEST>
            400:
                description: incorrect request body or unexpected user type
            401:
                description: could not find logged in Requester with given sessionId
    '''
    body = flask.globals.request.json
    try:
        if body['userType'] == 'Requester':
            get_own_requests_f = request_handler.get_requesters_own_requests
        elif body['userType'] == 'Volunteer':
            get_own_requests_f = request_handler.get_volunteers_own_requests
        else:
            raise UnexpectedUserTypeError
        return make_response(
            jsonify(
                get_own_requests_f(
                    session_id=body['sessionId']
                )
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UnexpectedUserTypeError:
        return make_response('Unexpected user type %s' % body['userType'], BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Requester with session id %s not found' % body['sessionId'], UNAUTHORIZED)


REQUEST_DOCSTRING = '''type: object
                                properties:
                                    id:
                                        type: string
                                    requester:
                                        type: string
                                        description: id of the requester of this request
                                    volunteer:
                                        type: string
                                        description: id of the volunteer handling this request (may be null if not yet assigned to a volunteer)
                                    status:
                                        type: number
                                        description: processing status of this request
                                    items:
                                        type: array
                                        items:
                                            type: object
                                            properties:
                                                item:
                                                    type: object
                                                    properties:
                                                        id:
                                                            type: string
                                                        name:
                                                            type: string
                                                        price:
                                                            type: number
                                                        category:
                                                            type: string
                                                        shop:
                                                            type: string
                                                            description: id of the shop
                                                amount:
                                                    type: number
                                                    description: amount of this item in the request
'''

get_open_requests.__doc__ = get_open_requests.__doc__.replace('<REQUEST>', REQUEST_DOCSTRING)
get_own_requests.__doc__ = get_own_requests.__doc__.replace('<REQUEST>', REQUEST_DOCSTRING)

