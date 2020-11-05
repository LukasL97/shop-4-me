from flask import Response, request, make_response, jsonify

from api.http_status import OK, BAD_REQUEST, UNAUTHORIZED, UNPROCESSABLE_ENTITY
from model.exception import UserSessionIdNotFoundError, UnexpectedNumberOfLocationsForAddressError
from model.shop import ShopHandler
from spec import DocumentedBlueprint

shop = DocumentedBlueprint('shop', __name__)


@shop.route('/shop', methods=['POST'])
def create_shop(shop_handler: ShopHandler) -> Response:
    '''
    ---
    post:
        summary: create a shop as a ShopOwner
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            name:
                                type: string
                                description: name of the created shop
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
                                description: session id of a logged in user of type ShopOwner
        responses:
            200:
                description: id of the successfully created shop
                content:
                    string:
                        schema:
                            type: string
                            description: shop id
            400:
                description: incorrect request body
            401:
                description: no ShopOwner with this session id found
            422:
                description: given address could not be resolved to exactly one geolocation via the external geocoding API
    '''
    body = request.json
    try:
        return make_response(
            shop_handler.create_shop(
                name=body['name'],
                street=body['address']['street'],
                zip=body['address']['zip'],
                country=body['address']['country'],
                session_id=body['sessionId']
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except UserSessionIdNotFoundError:
        return make_response('User of type ShopOwner with session id %s not found' % body['sessionId'], UNAUTHORIZED)
    except UnexpectedNumberOfLocationsForAddressError as error:
        return make_response('Address "%s" resolved to %d geolocations' % (error.address, error.number_of_locations), UNPROCESSABLE_ENTITY)


@shop.route('/shops', methods=['GET'])
def get_shops(shop_handler: ShopHandler) -> Response:
    '''
    ---
    get:
        summary: get all shops
        responses:
            200:
                description: list of all shops
                content:
                    array:
                        schema:
                            type: array
                            items:
                                type: object
                                properties:
                                    id:
                                        type: string
                                    name:
                                        type: string
                                    address:
                                        type: object
                                        properties:
                                            street:
                                                type: string
                                            zip:
                                                type: string
                                            country:
                                                type: string
                                            coordinates:
                                                type: object
                                                properties:
                                                    lat:
                                                        type: number
                                                        description: latitude
                                                    lng:
                                                        type: number
                                                        description: longitude
                                    owner:
                                        type: string
                                        description: id of the ShopOwner owning this shop
    '''
    return make_response(jsonify(shop_handler.get_shops()), OK)

