from unittest import TestCase
from unittest.mock import Mock

from bson import ObjectId

from dao.items_dao import ItemsDAO
from dao.shops_dao import ShopsDAO
from model.exception import UserSessionIdNotFoundError, ObjectIdNotFoundError, UnauthorizedAccessError
from model.image import Image
from model.item import Item, ItemHandler
from model.location.address import AddressHandler, Address
from model.product_details import ProductDetails
from model.shop import ShopHandler, Shop
from model.user import ShopOwnerHandler, ShopOwner
from test.model.util.stubs import AddressLocatorStub
from test.mongodb_integration_test_setup import get_empty_local_test_db


class ItemHandlerTest(TestCase):

    db = get_empty_local_test_db(['Items'])
    items_dao = ItemsDAO(db)
    shop_owner_handler = ShopOwnerHandler(None)
    shops_dao = ShopsDAO(db)
    address_handler = AddressHandler(None)
    shop_handler = ShopHandler(shops_dao, shop_owner_handler, address_handler)
    item_handler = ItemHandler(items_dao, shop_owner_handler, shop_handler)

    def setUp(self):
        self.items_dao.clear()
        self.shops_dao.clear()
        self.shop_owner_handler.active_user_sessions.clear()

    def test_add_item_correctly(self):
        session_id = 'someId'
        name = 'ItemName'
        price = 42.42
        category = 'Category'
        description = 'This is some item'
        attributes = {'att1': 42, 'att2': 'bla'}
        image_id = 'imageId'
        image_url = 'https://image.com'
        owner_id = str(ObjectId())
        owner = ShopOwner('login', 'pw', 'first', 'last', id=owner_id)
        self.shop_owner_handler.active_user_sessions[session_id] = owner
        shop = Shop('Shop', Address('', '', '', 0, 0), owner_id)
        shop_id = self.shops_dao.store_one(shop.to_db_object())
        item_id = self.item_handler.add_item(name, price, category, shop_id, description, attributes, image_id, image_url, session_id)
        items = self.items_dao.get_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(str(items[0]['_id']), item_id)
        self.assertEqual(items[0]['name'], name)
        self.assertEqual(items[0]['price'], price)
        self.assertEqual(items[0]['category'], category)
        self.assertEqual(str(items[0]['shop']), shop_id)
        self.assertEqual(items[0]['details']['description'], description)
        self.assertEqual(items[0]['details']['attributes'], attributes)
        self.assertEqual(items[0]['image']['id'], image_id)
        self.assertEqual(items[0]['image']['url'], image_url)

    def test_add_item_with_unknown_session_id(self):
        self.shop_owner_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.item_handler.add_item('ItemName', 42.42, 'Category', '5f7c28c6e979c6a33a1f3f79', 'description', {}, 'imageId', 'imageUrl', 'otherSessionId')

    def test_add_item_with_unknown_shop_id(self):
        session_id = 'sessionId'
        self.shop_owner_handler.active_user_sessions[session_id] = Mock()
        self.assertEqual(len(self.shops_dao.get_all()), 0)
        with self.assertRaises(ObjectIdNotFoundError):
            self.item_handler.add_item('ItemName', 42.42, 'Category', str(ObjectId()), 'description', {}, 'imageId', 'imageUrl', session_id)

    def test_add_item_with_incorrect_owner_id(self):
        session_id = 'sessionId'
        owner_id = str(ObjectId())
        other_owner_id = str(ObjectId())
        owner = ShopOwner('login', 'pw', 'first', 'last', id=other_owner_id)
        self.shop_owner_handler.active_user_sessions[session_id] = owner
        shop = Shop('Shop', Address('', '', '', 0, 0), owner_id)
        shop_id = self.shops_dao.store_one(shop.to_db_object())
        with self.assertRaises(UnauthorizedAccessError):
            self.item_handler.add_item('Item', 42.42, 'Category', shop_id, 'Description', {}, 'imageId', 'imageUrl', session_id)

    def test_get_items_by_shop_and_category(self):
        dao = ItemsDAO(self.db)
        category_a = 'CategoryA'
        category_b = 'CategoryB'
        shop_a = '5f7c28c6e979c6a33a1f3f79'
        shop_b = '5f7c2d96e48e242b81178822'
        item_1 = Item('Name1', 1.0, category_a, shop_a, ProductDetails('', {}), Image('', ''))
        item_2 = Item('Name2', 1.0, category_a, shop_b, ProductDetails('', {}), Image('', ''))
        item_3 = Item('Name3', 1.0, category_b, shop_a, ProductDetails('', {}), Image('', ''))
        item_4 = Item('Name4', 1.0, category_b, shop_b, ProductDetails('', {}), Image('', ''))
        for item in [item_1, item_2, item_3, item_4]:
            dao.store_one(item.to_db_object())
        items = self.item_handler.get_items_by_shop_and_category(None, None)
        self.assertEqual(len(items), 4)
        items = self.item_handler.get_items_by_shop_and_category(shop_a, category_a)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], item_1.name)
        items = self.item_handler.get_items_by_shop_and_category(shop_b, None)
        self.assertEqual(len(items), 2)
        self.assertEqual(len([i for i in items if i['name'] == item_2.name]), 1)
        self.assertEqual(len([i for i in items if i['name'] == item_4.name]), 1)
        items = self.item_handler.get_items_by_shop_and_category(None, category_b)
        self.assertEqual(len([i for i in items if i['name'] == item_3.name]), 1)
        self.assertEqual(len([i for i in items if i['name'] == item_4.name]), 1)