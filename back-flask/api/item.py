from flask import Response, request, make_response, jsonify

from api.http_status import OK, BAD_REQUEST, UNPROCESSABLE_ENTITY, UNAUTHORIZED
from model.exception import ShopDoesNotExistError, UserSessionIdNotFoundError, UnauthorizedAccessError
from model.item import ItemHandler
from spec import DocumentedBlueprint

item = DocumentedBlueprint('item', __name__)


@item.route('/items/findByShopAndCategory', methods=['GET'])
def find_by_shop_and_category(item_handler: ItemHandler) -> Response:
    '''
    ---
    get:
        summary: find items by the shop id and/or category
        parameters:
            -   name: shopId
                type: string
                description: the id of the shop that sells the items
                required: false
                in: query
            -   name: category
                type: string
                description: the category of the items
                required: false
                in: query
        responses:
            200:
                description: list of matching items
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
                                    price:
                                        type: number
                                    category:
                                        type: string
                                    shop:
                                        type: string
                                        description: id of the shop
    '''
    shop_id = request.args.get('shopId', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    return make_response(jsonify(item_handler.get_items_by_shop_and_category(shop_id, category)), OK)


@item.route('/item', methods=['POST'])
def add_item(item_handler: ItemHandler) -> Response:
    '''
    ---
    post:
        summary: add an item to a shop
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            item:
                                type: object
                                properties:
                                    name:
                                        type: string
                                    price:
                                        type: number
                                    category:
                                        type: string
                                    shop:
                                        type: string
                                        description: id of the shop
                            sessionId:
                                type: string
                                description: session id of a logged in user of type ShopOwner
        responses:
            200:
                description: id of the successfully added item
                content:
                    string:
                        schema:
                            type: string
                            description: item id
            400:
                description: incorrect request body
            401:
                description: session id not found or session id does not refer to correct ShopOwner
            422:
                description: shop does not exist
    '''
    body = request.json
    try:
        return make_response(
            item_handler.add_item(
                name=body['item']['name'],
                price=body['item']['price'],
                category=body['item']['category'],
                shop=body['item']['shop'],
                session_id=body['sessionId']
            ),
            OK
        )
    except KeyError:
        return make_response('Request body did not contain required information', BAD_REQUEST)
    except ShopDoesNotExistError:
        return make_response('Tried adding item to non-existing shop', UNPROCESSABLE_ENTITY)
    except UserSessionIdNotFoundError:
        return make_response('User of type ShopOwner with session id %s not found' % body['sessionId'], UNAUTHORIZED)
    except UnauthorizedAccessError:
        return make_response('User with session id %s does not own shop %s' % (body['sessionId'], body['shop']), UNAUTHORIZED)
