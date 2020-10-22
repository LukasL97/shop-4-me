from unittest import TestCase
from unittest.mock import Mock

from dao.items_dao import ItemsDAO
from model.exception import UserSessionIdNotFoundError
from model.item import Item, ItemHandler
from model.user import ShopOwnerHandler
from test.mongodb_integration_test_setup import get_empty_local_test_db


class ItemHandlerTest(TestCase):

    db = get_empty_local_test_db(['Items'])
    dao = ItemsDAO(db)
    shop_owner_handler = ShopOwnerHandler(None)
    item_handler = ItemHandler(dao, shop_owner_handler)

    def setUp(self):
        self.dao.clear()
        self.shop_owner_handler.active_user_sessions.clear()

    def test_add_item_correctly(self):
        session_id = 'someId'
        name = 'ItemName'
        price = 42.42
        category = 'Category'
        shop = '5f7c28c6e979c6a33a1f3f79'
        self.shop_owner_handler.active_user_sessions[session_id] = Mock()
        item_id = self.item_handler.add_item(name, price, category, shop, session_id)
        items = self.dao.get_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(str(items[0]['_id']), item_id)
        self.assertEqual(items[0]['name'], name)
        self.assertEqual(items[0]['price'], price)
        self.assertEqual(items[0]['category'], category)
        self.assertEqual(str(items[0]['shop']), shop)

    def test_add_item_with_unknown_session_id(self):
        self.shop_owner_handler.active_user_sessions['someSessionId'] = Mock()
        with self.assertRaises(UserSessionIdNotFoundError):
            self.item_handler.add_item('ItemName', 42.42, 'Category', '5f7c28c6e979c6a33a1f3f79', 'otherSessionId')

    def test_get_items_by_shop_and_category(self):
        dao = ItemsDAO(self.db)
        category_a = 'CategoryA'
        category_b = 'CategoryB'
        shop_a = '5f7c28c6e979c6a33a1f3f79'
        shop_b = '5f7c2d96e48e242b81178822'
        item_1 = Item('Name1', 1.0, category_a, shop_a)
        item_2 = Item('Name2', 1.0, category_a, shop_b)
        item_3 = Item('Name3', 1.0, category_b, shop_a)
        item_4 = Item('Name4', 1.0, category_b, shop_b)
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