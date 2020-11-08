import sys

import pymongo
from pymongo.database import Database

from dao.items_dao import ItemsDAO
from dao.requests_dao import RequestsDAO
from dao.shops_dao import ShopsDAO
from dao.time_frames_dao import TimeFramesDAO
from dao.users_dao import RequestersDAO, VolunteersDAO, ShopOwnersDAO
from model.item import ItemHandler
from model.location.address import AddressHandler
from model.location.geocoding import AddressLocator
from model.request import RequestHandler
from model.shop import ShopHandler
from model.time_frame import TimeFrameHandler
from model.user import RequesterHandler, VolunteerHandler, ShopOwnerHandler

try:
    MONGODB_URI = sys.argv[1]
except IndexError:
    MONGODB_URI = 'localhost:27017'

client = pymongo.MongoClient(MONGODB_URI)
db: Database = client.shopme_db

for collection in db.list_collection_names():
    db.drop_collection(collection)

db.create_collection('Requesters')
db.create_collection('Volunteers')
db.create_collection('ShopOwners')
db.create_collection('Requests')
db.create_collection('Items')
db.create_collection('Shops')
db.create_collection('TimeFrames')

print(db.list_collection_names())

requesters_dao = RequestersDAO(db)
volunteers_dao = VolunteersDAO(db)
shop_owners_dao = ShopOwnersDAO(db)
requests_dao = RequestsDAO(db)
items_dao = ItemsDAO(db)
shops_dao = ShopsDAO(db)
time_frames_dao = TimeFramesDAO(db)

address_handler = AddressHandler(AddressLocator())
requester_handler = RequesterHandler(requesters_dao, address_handler)
volunteer_handler = VolunteerHandler(volunteers_dao)
shop_owner_handler = ShopOwnerHandler(shop_owners_dao)
shop_handler = ShopHandler(shops_dao, shop_owner_handler, address_handler)
item_handler = ItemHandler(items_dao, shop_owner_handler, shop_handler)
request_handler = RequestHandler(requests_dao, item_handler, requester_handler, volunteer_handler, address_handler)
time_frame_handler = TimeFrameHandler(time_frames_dao, volunteer_handler, request_handler)

# USERS

requester_1 = requester_handler.register('test@test.com', 'test', 'test', 'McTestface')
requester_2 = requester_handler.register('some@requester.com', 'password', 'Reques', 'Ter')
requester_3 = requester_handler.register('another@requester.com', '1234', 'Peter', 'Turner')

requester_handler.set_address('Junailijankuja 5B', '00520', 'Finland', requester_1)
requester_handler.set_address('Unioninkatu 29', '00170', 'Finland', requester_2)
requester_handler.set_address('Wildunger Straße 6', '60487', 'Germany', requester_3)

volunteer_1 = volunteer_handler.register('test@test.com', 'test', 'Volunteer', 'McVolunteerface')
volunteer_2 = volunteer_handler.register('volunteer@test.com', 'test', 'Ville', 'Volunteer')
volunteer_3 = volunteer_handler.register('another@volunteer.com', 'volunteer', 'Another', 'Volunteer')

shop_owner_1 = shop_owner_handler.register('sotest@test.com', 'sotest', 'Shop', 'Owner')
shop_owner_2 = shop_owner_handler.register('shop@owner.com', 'shopowner', 'Shop', 'Owner')
shop_owner_3 = shop_owner_handler.register('shopowner@test.com', 'test', 'Shop', 'Owner')

# SHOPS AND ITEMS

shop_1 = shop_handler.create_shop('K Market', 'Fredikanterassi 1', '00520', 'Finland', shop_owner_1)
shop_2 = shop_handler.create_shop('Prisma', 'Iso Omena', '02230', 'Finland', shop_owner_2)
shop_3 = shop_handler.create_shop('Edeka', 'An der Taunuseisenbahn 7', '65795', 'Germany', shop_owner_3)

item_01 = item_handler.add_item('Pizza', 3.95, 'Food', shop_1, 'Delicious Pizza', {'calories': 'a lot'}, 'imageId', 'image.com', shop_owner_1)
item_02 = item_handler.add_item('Beer 0.5L', 2.95, 'Drink', shop_1, '5% alcohol', {}, 'imageId', 'image.com', shop_owner_1)
item_03 = item_handler.add_item('Apple', 0.80, 'Food', shop_1, 'From Italy', {}, 'imageId', 'image.com', shop_owner_1)
item_04 = item_handler.add_item('Cheese', 1.50, 'Food', shop_1, 'Delicious cheese from Switzerland', {}, 'imageId', 'image.com', shop_owner_1)
item_05 = item_handler.add_item('Salami', 1.50, 'Food', shop_1, 'Just salami', {}, 'imageId', 'image.com', shop_owner_1)
item_06 = item_handler.add_item('Spaghetti 1kg', 1.95, 'Food', shop_1, 'Spaghetti', {}, 'imageId', 'image.com', shop_owner_1)
item_07 = item_handler.add_item('Salt', 0.95, 'Food', shop_1, 'Salt', {}, 'imageId', 'image.com', shop_owner_1)
item_08 = item_handler.add_item('Coca Cola 1.5L', 1.95, 'Drink', shop_1, 'Now with even more sugar', {'calories': '1000000 kcal'}, 'imageId', 'image.com', shop_owner_1)
item_09 = item_handler.add_item('Milk 1L', 1.0, 'Drink', shop_1, 'From happy cows', {}, 'imageId', 'image.com', shop_owner_1)
item_10 = item_handler.add_item('Eggs (6)', 1.95, 'Food', shop_1, 'From happy chickens', {}, 'imageId', 'image.com', shop_owner_1)

item_11 = item_handler.add_item('Pepper', 0.65, 'Food', shop_2, 'Pepper', {}, 'imageId', 'image.com', shop_owner_2)
item_12 = item_handler.add_item('Rice 1kg', 1.80, 'Food', shop_2, 'Rice', {}, 'imageId', 'image.com', shop_owner_2)
item_13 = item_handler.add_item('Banana', 0.30, 'Food', shop_2, 'Healthy bananas from South America', {}, 'imageId', 'image.com', shop_owner_2)
item_14 = item_handler.add_item('Orange', 0.35, 'Food', shop_2, 'Spanish oranges', {'color': 'orange'}, 'imageId', 'image.com', shop_owner_2)
item_15 = item_handler.add_item('Bread', 1.20, 'Food', shop_2, 'Gluten-free', {}, 'imageId', 'image.com', shop_owner_2)
item_16 = item_handler.add_item('Salmon', 3.80, 'Food', shop_2, 'Fresh and regional', {}, 'imageId', 'image.com', shop_owner_2)
item_17 = item_handler.add_item('Ice Cream', 3.50, 'Food', shop_2, 'Cold and delicious', {'flavour': 'chocolate'}, 'imageId', 'image.com', shop_owner_2)
item_18 = item_handler.add_item('Pringles', 2.50, 'Food', shop_2, 'Pringles 190g', {'calories': '500 kcal'}, 'imageId', 'image.com', shop_owner_2)
item_19 = item_handler.add_item('Vodka', 15.95, 'Drink', shop_2, 'From Mother Russia with 120% alcohol', {}, 'imageId', 'image.com', shop_owner_2)
item_20 = item_handler.add_item('Olive Oil', 1.95, 'Food', shop_2, 'From Greece', {}, 'imageId', 'image.com', shop_owner_2)

item_21 = item_handler.add_item('Water', 0.80, 'Drink', shop_3, 'Water', {}, 'imageId', 'image.com', shop_owner_3)
item_22 = item_handler.add_item('Cookies', 1.45, 'Food', shop_3, 'Delicious chocolate cookies', {'count': '8'}, 'imageId', 'image.com', shop_owner_3)
item_23 = item_handler.add_item('Toilet cleaner', 3.80, 'Cleaning', shop_3, 'Do not drink!', {}, 'imageId', 'image.com', shop_owner_3)
item_24 = item_handler.add_item('Sponge', 0.20, 'Cleaning', shop_3, 'Sponge for cleaning', {}, 'imageId', 'image.com', shop_owner_3)
item_25 = item_handler.add_item('Dish soap', 0.99, 'Cleaning', shop_3, 'Dish soap', {}, 'imageId', 'image.com', shop_owner_3)
item_26 = item_handler.add_item('Pear', 0.89, 'Food', shop_3, 'From Spain', {}, 'imageId', 'image.com', shop_owner_3)
item_27 = item_handler.add_item('Beans', 1.89, 'Food', shop_3, 'Delicious green beans', {}, 'imageId', 'image.com', shop_owner_3)
item_28 = item_handler.add_item('Trout', 6.99, 'Food', shop_3, 'Fresh and regional', {}, 'imageId', 'image.com', shop_owner_3)
item_29 = item_handler.add_item('Pineapple', 6.99, 'Food', shop_3, 'Do not put on pizza!', {}, 'imageId', 'image.com', shop_owner_3)
item_30 = item_handler.add_item('Vinegar', 1.79, 'Food', shop_3, 'Vinegar from Italy', {}, 'imageId', 'image.com', shop_owner_3)

# REQUESTS

request_1 = request_handler.create_request([{'id': item_01, 'amount': 3}, {'id': item_02, 'amount': 1}, {'id': item_03, 'amount': 2}], requester_1)
request_2 = request_handler.create_request([{'id': item_07, 'amount': 10}, {'id': item_08, 'amount': 5}], requester_1)

request_handler.submit_request(request_1, requester_1)
request_handler.submit_request(request_2, requester_1)

request_handler.accept_request(request_1, volunteer_1)

# TIME FRAMES

time_frame_1 = time_frame_handler.add_time_frame('2020-11-15 12:00:00', '2020-11-15 15:00:00', volunteer_1)
time_frame_2 = time_frame_handler.add_time_frame('2020-11-20 10:00:00', '2020-11-15 12:00:00', volunteer_1)

time_frame_handler.add_request_to_time_frame(time_frame_1, request_1, volunteer_1)



