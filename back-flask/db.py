
import pymongo
from pymongo.database import Database

MONGODB_URI = 'mongodb+srv://asabeneh:Asab123123123@shopme.azwx2.mongodb.net/shop4me_db?retryWrites=true&w=majority'

client = pymongo.MongoClient(MONGODB_URI)
db: Database = client.shopme_db
