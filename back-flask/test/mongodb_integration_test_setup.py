from typing import List

import pymongo
from pymongo.database import Database

MONGODB_URI = 'localhost:27017'

def get_empty_local_test_db(collections: List[str]) -> Database:
    client = pymongo.MongoClient(MONGODB_URI)
    db: Database = client.shopme_db
    for collection in db.list_collection_names():
        db.drop_collection(collection)
    for collection in collections:
        db.create_collection(collection)
    return db
