from flask import Flask
import pymongo
import os
app = Flask(__name__)

# MongoDB Database connection
# Databse name, shopme_db

MONGODB_URI = 'mongodb+srv://asabeneh:Asab123123123@cluster0.8zud1.mongodb.net/shopme_db?retryWrites=true&w=majority'

client = pymongo.MongoClient(MONGODB_URI)
db = client.shopme_db



@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    # for deployment
    # to make it work for both production and development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
# Run with export FLASK_APP=main.py; python -m flask run
