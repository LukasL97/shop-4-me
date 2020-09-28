from flask import Flask, Response
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo
import os
app = Flask(__name__)
# import requesters 
# import requests
# import volunteers
# import shop_owners
# import shops

# print(requesters.requesters)

# MongoDB Database connection
# Databse name, shopme_db

MONGODB_URI = 'mongodb+srv://asabeneh:Asab123123123@shopme.azwx2.mongodb.net/shop4me_db?retryWrites=true&w=majority'

client = pymongo.MongoClient(MONGODB_URI)
db = client.shop4me_db


# for vol in volunteers.volunteers:
#     db.volunteers.insert_one(vol)

@app.route('/')
def hello_world():
    return 'Hello, World!'



if __name__ == '__main__':
    # for deployment
    # to make it work for both production and development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
# Run with export FLASK_APP=main.py; python -m flask run
