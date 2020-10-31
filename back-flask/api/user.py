
from flask import request, Response, make_response

from api.http_status import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, CONFLICT, UNPROCESSABLE_ENTITY
from model.exception import UnexpectedUserTypeError, UserNotFoundError, IncorrectPasswordError, \
    UserAlreadyRegisteredError, UserSessionIdNotFoundError, UnexpectedNumberOfLocationsForAddressError
from model.user import UserHandlerResolver, RequesterHandler
from spec import DocumentedBlueprint

user = DocumentedBlueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login(resolver: UserHandlerResolver) -> Response:
    '''
    ---
    post:
        summary: login a user
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            userType:
                                type: string
                                description: either "Requester", "Volunteer" or "ShopOwner"
                            loginName:
                                type: string
                            password:
                                type: string
        responses:
            200:
                description: session id for successful login
                content:
                    string:
                        schema:
                            type: string
                            description: session id for this login
            400:
                description: unexpected user type or incorrect request body
            401:
                description: incorrect password
            404:
                description: user not found
    '''
    user_data = request.json
    try:
        user_handler = resolver.get(user_data['userType'])
        return make_response(user_handler.login(user_data['loginName'], user_data['password']), OK)
    except UnexpectedUserTypeError:
        return make_response('Unexpected user type %s' % user_data['userType'], BAD_REQUEST)
    except UserNotFoundError:
        return make_response('User %s not found' % user_data['loginName'], NOT_FOUND)
    except IncorrectPasswordError:
        return make_response('Incorrect password', UNAUTHORIZED)
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)


@user.route('/register', methods=['POST'])
def register(resolver: UserHandlerResolver) -> Response:
    '''
    ---
    post:
        summary: register a user
        description: user is logged in after registration immediately
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            userType:
                                type: string
                                description: either "Requester", "Volunteer" or "ShopOwner"
                            loginName:
                                type: string
                            password:
                                type: string
                            firstName:
                                type: string
                            lastName:
                                type: string
        responses:
            200:
                description: session id for successful registration and login
                content:
                    string:
                        schema:
                            type: string
                            description: session id for this login
            400:
                description: unexpected user type or incorrect request body
            409:
                description: user with this loginName already registered
    '''
    user_data = request.json
    try:
        user_handler = resolver.get(user_data['userType'])
        return make_response(user_handler.register(
            login_name=user_data['loginName'],
            password=user_data['password'],
            first_name=user_data['firstName'],
            last_name=user_data['lastName']
        ), OK)
    except UnexpectedUserTypeError:
        return make_response('Unexpected user type %s' % user_data['userType'], BAD_REQUEST)
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserAlreadyRegisteredError:
        return make_response('Login name %s is already used' % user_data['loginName'], CONFLICT)


@user.route('/logout', methods=['DELETE'])
def logout(resolver: UserHandlerResolver) -> Response:
    '''
    ---
    delete:
        summary: logout a logged in user
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            userType:
                                type: string
                                description: either "Requester", "Volunteer" or "ShopOwner"
                            sessionId:
                                type: string
                                description: session id of the user that is to be logged out
        responses:
            200:
                description: logout successful
            400:
                description: unexpected user type or incorrect request body
            404:
                description: session id did not refer to any logged in user of this type
    '''
    user_data = request.json
    try:
        user_handler = resolver.get(user_data['userType'])
        return make_response(user_handler.logout(
            session_id=user_data['sessionId']
        ), OK)
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type %s with session id %s not found' % (user_data['userType'], user_data['sessionId']), NOT_FOUND)


@user.route('/requester/address', methods=['PUT'])
def set_requester_address(requester_handler: RequesterHandler) -> Response:
    '''
    ---
    put:
        summary: set your own address as a requester
        description: The address is resolved to a geolocation (latitude, longitude) internally, via an external geocoding API.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            address:
                                type: object
                                properties:
                                    street:
                                        type: string
                                        description: street incl. house number in the format common in the according country (e.g. "Junailijankuja 5B")
                                    zip:
                                        type: string
                                        description: zip code (e.g. "00520")
                                    country:
                                        type: string
                                        description: country name in english (but national language should also work) (e.g. "Finland")
                            sessionId:
                                type: string
                                description: session id of the requester setting their address
        responses:
            200:
                description: address set successfully
            400:
                description: incorrect request body
            404:
                description: session id did not refer to any logged in user of type Requester
            422:
                description: the given address could not be resolved to exactly one geolocation via the external geocoding API
    '''
    user_data = request.json
    try:
        return make_response(requester_handler.set_address(
            street=user_data['address']['street'],
            zip=user_data['address']['zip'],
            country=user_data['address']['country'],
            session_id=user_data['sessionId']
        ), OK)
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type Requester with session id %s not found' % user_data['sessionId'], NOT_FOUND)
    except UnexpectedNumberOfLocationsForAddressError as error:
        return make_response('Address "%s" resolved to %d geolocations' % (error.address, error.number_of_locations), UNPROCESSABLE_ENTITY)
