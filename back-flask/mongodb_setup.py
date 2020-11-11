import sys

import os
import cloudinary
import pymongo
from cloudinary import uploader
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
from paths import ROOT

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

# ITEM IMAGES

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

images_base_path = ROOT / 'back-flask' / 'dummy_data' / 'images'

image_01 = uploader.upload(str(images_base_path / 'item_01.jpg'))
image_02 = uploader.upload(str(images_base_path / 'item_02.jpg'))
image_03 = uploader.upload(str(images_base_path / 'item_03.jpg'))
image_04 = uploader.upload(str(images_base_path / 'item_04.jpg'))
image_05 = uploader.upload(str(images_base_path / 'item_05.jpg'))
image_06 = uploader.upload(str(images_base_path / 'item_06.jpg'))
image_07 = uploader.upload(str(images_base_path / 'item_07.jpg'))
image_08 = uploader.upload(str(images_base_path / 'item_08.jpg'))
image_09 = uploader.upload(str(images_base_path / 'item_09.jpg'))
image_10 = uploader.upload(str(images_base_path / 'item_10.jpg'))
image_11 = uploader.upload(str(images_base_path / 'item_11.jpg'))
image_12 = uploader.upload(str(images_base_path / 'item_12.jpg'))
image_13 = uploader.upload(str(images_base_path / 'item_13.jpg'))
image_14 = uploader.upload(str(images_base_path / 'item_14.jpg'))
image_15 = uploader.upload(str(images_base_path / 'item_15.jpg'))
image_16 = uploader.upload(str(images_base_path / 'item_16.jpg'))
image_17 = uploader.upload(str(images_base_path / 'item_17.jpg'))
image_18 = uploader.upload(str(images_base_path / 'item_18.jpg'))
image_19 = uploader.upload(str(images_base_path / 'item_19.jpg'))
image_20 = uploader.upload(str(images_base_path / 'item_20.jpg'))
image_21 = uploader.upload(str(images_base_path / 'item_21.jpg'))
image_22 = uploader.upload(str(images_base_path / 'item_22.jpg'))
image_23 = uploader.upload(str(images_base_path / 'item_23.jpg'))
image_24 = uploader.upload(str(images_base_path / 'item_24.jpg'))
image_25 = uploader.upload(str(images_base_path / 'item_25.jpg'))
image_26 = uploader.upload(str(images_base_path / 'item_26.jpg'))
image_27 = uploader.upload(str(images_base_path / 'item_27.jpg'))
image_28 = uploader.upload(str(images_base_path / 'item_28.jpg'))
image_29 = uploader.upload(str(images_base_path / 'item_29.jpg'))
image_30 = uploader.upload(str(images_base_path / 'item_30.jpg'))

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

item_01 = item_handler.add_item('Pizza', 3.95, 'Food', shop_1, 'Delicious Pizza', {'calories': 'a lot'}, image_01['public_id'], image_01['secure_url'], shop_owner_1)
item_02 = item_handler.add_item('Beer 0.5L', 2.95, 'Drink', shop_1, '5% alcohol', {}, image_02['public_id'], image_02['secure_url'], shop_owner_1)
item_03 = item_handler.add_item('Apple', 0.80, 'Food', shop_1, 'From Italy', {}, image_03['public_id'], image_03['secure_url'], shop_owner_1)
item_04 = item_handler.add_item('Cheese', 1.50, 'Food', shop_1, 'Delicious cheese from Switzerland', {}, image_04['public_id'], image_04['secure_url'], shop_owner_1)
item_05 = item_handler.add_item('Salami', 1.50, 'Food', shop_1, 'Just salami', {}, image_05['public_id'], image_05['secure_url'], shop_owner_1)
item_06 = item_handler.add_item('Spaghetti 1kg', 1.95, 'Food', shop_1, 'Spaghetti', {}, image_06['public_id'], image_06['secure_url'], shop_owner_1)
item_07 = item_handler.add_item('Salt', 0.95, 'Food', shop_1, 'Salt', {}, image_07['public_id'], image_07['secure_url'], shop_owner_1)
item_08 = item_handler.add_item('Coca Cola 1.5L', 1.95, 'Drink', shop_1, 'Now with even more sugar', {'calories': '1000000 kcal'}, image_08['public_id'], image_08['secure_url'], shop_owner_1)
item_09 = item_handler.add_item('Milk 1L', 1.0, 'Drink', shop_1, 'From happy cows', {}, image_09['public_id'], image_09['secure_url'], shop_owner_1)
item_10 = item_handler.add_item('Eggs (6)', 1.95, 'Food', shop_1, 'From happy chickens', {}, image_10['public_id'], image_10['secure_url'], shop_owner_1)

item_11 = item_handler.add_item('Pepper', 0.65, 'Food', shop_2, 'Pepper', {}, image_11['public_id'], image_11['secure_url'], shop_owner_2)
item_12 = item_handler.add_item('Rice 1kg', 1.80, 'Food', shop_2, 'Rice', {}, image_12['public_id'], image_12['secure_url'], shop_owner_2)
item_13 = item_handler.add_item('Banana', 0.30, 'Food', shop_2, 'Healthy bananas from South America', {}, image_13['public_id'], image_13['secure_url'], shop_owner_2)
item_14 = item_handler.add_item('Orange', 0.35, 'Food', shop_2, 'Spanish oranges', {'color': 'orange'}, image_14['public_id'], image_14['secure_url'], shop_owner_2)
item_15 = item_handler.add_item('Bread', 1.20, 'Food', shop_2, 'Gluten-free', {}, image_15['public_id'], image_15['secure_url'], shop_owner_2)
item_16 = item_handler.add_item('Salmon', 3.80, 'Food', shop_2, 'Fresh and regional', {}, image_16['public_id'], image_16['secure_url'], shop_owner_2)
item_17 = item_handler.add_item('Ice Cream', 3.50, 'Food', shop_2, 'Cold and delicious', {'flavour': 'chocolate'}, image_17['public_id'], image_17['secure_url'], shop_owner_2)
item_18 = item_handler.add_item('Pringles', 2.50, 'Food', shop_2, 'Pringles 190g', {'calories': '500 kcal'}, image_18['public_id'], image_18['secure_url'], shop_owner_2)
item_19 = item_handler.add_item('Vodka', 15.95, 'Drink', shop_2, 'From Mother Russia with 120% alcohol', {}, image_19['public_id'], image_19['secure_url'], shop_owner_2)
item_20 = item_handler.add_item('Olive Oil', 1.95, 'Food', shop_2, 'From Greece', {}, image_20['public_id'], image_20['secure_url'], shop_owner_2)

item_21 = item_handler.add_item('Water', 0.80, 'Drink', shop_3, 'Water', {}, image_21['public_id'], image_21['secure_url'], shop_owner_3)
item_22 = item_handler.add_item('Cookies', 1.45, 'Food', shop_3, 'Delicious chocolate cookies', {'count': '8'}, image_22['public_id'], image_22['secure_url'], shop_owner_3)
item_23 = item_handler.add_item('Toilet cleaner', 3.80, 'Cleaning', shop_3, 'Do not drink!', {}, image_23['public_id'], image_23['secure_url'], shop_owner_3)
item_24 = item_handler.add_item('Sponge', 0.20, 'Cleaning', shop_3, 'Sponge for cleaning', {}, image_24['public_id'], image_24['secure_url'], shop_owner_3)
item_25 = item_handler.add_item('Dish soap', 0.99, 'Cleaning', shop_3, 'Dish soap', {}, image_25['public_id'], image_25['secure_url'], shop_owner_3)
item_26 = item_handler.add_item('Pear', 0.89, 'Food', shop_3, 'From Spain', {}, image_26['public_id'], image_26['secure_url'], shop_owner_3)
item_27 = item_handler.add_item('Beans', 1.89, 'Food', shop_3, 'Delicious green beans', {}, image_27['public_id'], image_27['secure_url'], shop_owner_3)
item_28 = item_handler.add_item('Trout', 6.99, 'Food', shop_3, 'Fresh and regional', {}, image_28['public_id'], image_28['secure_url'], shop_owner_3)
item_29 = item_handler.add_item('Pineapple', 6.99, 'Food', shop_3, 'Do not put on pizza!', {}, image_29['public_id'], image_29['secure_url'], shop_owner_3)
item_30 = item_handler.add_item('Vinegar', 1.79, 'Food', shop_3, 'Vinegar from Italy', {}, image_30['public_id'], image_30['secure_url'], shop_owner_3)

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



