import flask
from flask import Response, make_response, jsonify

from api.http_status import OK, BAD_REQUEST, UNAUTHORIZED, UNPROCESSABLE_ENTITY
from model.exception import UserSessionIdNotFoundError, ObjectIdNotFoundError
from model.request import Request
from spec import DocumentedBlueprint

request = DocumentedBlueprint('request', __name__)


@request.route('/request', methods=['POST'])
def create_request() -> Response:
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
            Request.create_request(
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


@request.route('/request/own', methods=['GET'])
def get_requesters_own_requests() -> Response:
    '''
    ---
    get:
        summary: get a list of your own requests as a Requester
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            sessionId:
                                type: string
                                description: session id of a logged in user of type Requester
        responses:
            200:
                description: list of all requests created by this Requester with items directly inlined
                content:
                    array:
                        schema:
                            type: array
                            items:
                                type: object
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
            400:
                description: incorrect request body
            401:
                description: could not find logged in Requester with given sessionId
    '''
    body = flask.globals.request.json
    try:
        return make_response(
            jsonify(
                Request.get_requesters_own_requests(
                    session_id=body['sessionId']
                )
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Requester with session id %s not found' % body['sessionId'], UNAUTHORIZED)
