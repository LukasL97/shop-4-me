from unittest import TestCase

from bson import ObjectId

from dao.shops_dao import ShopsDAO
from model.exception import UserSessionIdNotFoundError, UnexpectedNumberOfLocationsForAddressError
from model.location.address import AddressHandler, Address
from model.shop import ShopHandler, Shop
from model.user import ShopOwnerHandler, ShopOwner
from test.model.util.stubs import AddressLocatorStub
from test.mongodb_integration_test_setup import get_empty_local_test_db


class ShopHandlerTest(TestCase):

    db = get_empty_local_test_db(['Shops'])
    dao = ShopsDAO(db)
    shop_owner_handler = ShopOwnerHandler(None)
    locator = AddressLocatorStub()
    address_handler = AddressHandler(locator)
    shop_handler = ShopHandler(dao, shop_owner_handler, address_handler)

    def setUp(self):
        self.dao.clear()
        self.shop_owner_handler.active_user_sessions.clear()

    def test_create_shop_correctly(self):
        session_id = 'sessionId'
        shop_owner_id = str(ObjectId())
        shop_owner = ShopOwner('login', 'pw', 'first', 'last', shop_owner_id)
        self.shop_owner_handler.active_user_sessions[session_id] = shop_owner
        shop_name = 'ShopName'
        id = self.shop_handler.create_shop(shop_name, self.locator.valid_street_1, self.locator.valid_zip_1, self.locator.valid_country_1, session_id)
        shops = self.dao.get_all()
        self.assertEqual(len(shops), 1)
        self.assertEqual(str(shops[0]['_id']), id)
        self.assertEqual(shops[0]['name'], shop_name)
        self.assertEqual(shops[0]['address']['street'], self.locator.valid_street_1)
        self.assertEqual(shops[0]['address']['zip'], self.locator.valid_zip_1)
        self.assertEqual(shops[0]['address']['country'], self.locator.valid_country_1)
        self.assertEqual(shops[0]['address']['coordinates']['lat'], self.locator.lat_1)
        self.assertEqual(shops[0]['address']['coordinates']['lng'], self.locator.lng_1)
        self.assertEqual(str(shops[0]['owner']), shop_owner_id)

    def test_create_shop_with_unknown_session_id(self):
        self.assertEqual(len(self.shop_owner_handler.active_user_sessions), 0)
        with self.assertRaises(UserSessionIdNotFoundError):
            self.shop_handler.create_shop('ShopName', self.locator.valid_street_1, self.locator.valid_zip_1, self.locator.valid_country_1, 'sessionId')

    def test_create_shop_with_non_locatable_address(self):
        session_id = 'sessionId'
        shop_owner_id = str(ObjectId())
        shop_owner = ShopOwner('login', 'pw', 'first', 'last', shop_owner_id)
        self.shop_owner_handler.active_user_sessions[session_id] = shop_owner
        with self.assertRaises(UnexpectedNumberOfLocationsForAddressError):
            self.shop_handler.create_shop('ShopName', 'Unknown Street', '00000', 'Nomansland', session_id)

    def test_get_shops_correctly(self):
        address_1 = Address('Street 1', '12345', 'Country 1', 42.42, 13.37)
        address_2 = Address('Street 2', '54321', 'Country 2', 8.15, 44.44)
        shop_1 = Shop('Shop 1', address_1, str(ObjectId()))
        shop_2 = Shop('Shop 2', address_2, str(ObjectId()))
        shop_1_id = self.dao.store_one(shop_1.to_db_object())
        shop_2_id = self.dao.store_one(shop_2.to_db_object())
        shops = self.shop_handler.get_shops()
        self.assertEqual(len(shops), 2)
        self.assertIn(shop_1_id, [shop['id'] for shop in shops])
        self.assertIn(shop_2_id, [shop['id'] for shop in shops])
