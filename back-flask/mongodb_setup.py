import sys

import pymongo
from pymongo.database import Database

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

print(db.list_collection_names())
