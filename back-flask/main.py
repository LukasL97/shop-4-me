import os

from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton, Binder

from api.item import item
from api.request import request
from api.shop import shop
from api.time_frame import time_frame
from api.user import user
from dao.items_dao import ItemsDAO
from dao.requests_dao import RequestsDAO
from dao.shops_dao import ShopsDAO
from dao.time_frames_dao import TimeFramesDAO
from dao.users_dao import RequestersDAO, VolunteersDAO, ShopOwnersDAO
from db import db
from model.item import ItemHandler
from model.location.address import AddressHandler
from model.location.geocoding import AddressLocator
from model.request import RequestHandler
from model.shop import ShopHandler
from model.time_frame import TimeFrameHandler
from model.user import RequesterHandler, VolunteerHandler, ShopOwnerHandler, UserHandlerResolver
from spec import get_spec_as_html

def configure_model_handlers(binder: Binder) -> None:
    binder.bind(RequesterHandler, to=RequesterHandler, scope=singleton)
    binder.bind(VolunteerHandler, to=VolunteerHandler, scope=singleton)
    binder.bind(ShopOwnerHandler, to=ShopOwnerHandler, scope=singleton)
    binder.bind(UserHandlerResolver, to=UserHandlerResolver, scope=singleton)
    binder.bind(ItemHandler, to=ItemHandler, scope=singleton)
    binder.bind(RequestHandler, to=RequestHandler, scope=singleton)
    binder.bind(AddressLocator, to=AddressLocator, scope=singleton)
    binder.bind(AddressHandler, to=AddressHandler, scope=singleton)
    binder.bind(TimeFrameHandler, to=TimeFrameHandler, scope=singleton)
    binder.bind(ShopHandler, to=ShopHandler, scope=singleton)

def configure_daos(binder: Binder) -> None:
    binder.bind(RequestersDAO, to=RequestersDAO(db), scope=singleton)
    binder.bind(VolunteersDAO, to=VolunteersDAO(db), scope=singleton)
    binder.bind(ShopOwnersDAO, to=ShopOwnersDAO(db), scope=singleton)
    binder.bind(ItemsDAO, to=ItemsDAO(db), scope=singleton)
    binder.bind(RequestsDAO, to=RequestsDAO(db), scope=singleton)
    binder.bind(TimeFramesDAO, to=TimeFramesDAO(db), scope=singleton)
    binder.bind(ShopsDAO, to=ShopsDAO(db), scope=singleton)

app = Flask(__name__)
CORS(app)
app.config['CORS_ORIGINS'] = 'http://localhost:3000'

app.register_blueprint(user)
app.register_blueprint(item)
app.register_blueprint(request)
app.register_blueprint(time_frame)
app.register_blueprint(shop)

FlaskInjector(app=app, modules=[configure_model_handlers, configure_daos])

@app.route('/')
def get_api_spec():
    return get_spec_as_html()

if __name__ == '__main__':
    # for deployment
    # to make it work for both production and development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
# Run with export FLASK_APP=main.py; python -m flask run
