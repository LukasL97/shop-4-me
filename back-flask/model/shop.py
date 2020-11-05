from typing import Optional, Dict, Any, List

from bson import ObjectId
from injector import inject

from dao.shops_dao import ShopsDAO
from model.abstract_model import AbstractModel, AbstractHandler
from model.location.address import Address, AddressHandler
from model.user import ShopOwnerHandler


class Shop(AbstractModel):

    def __init__(self, name: str, address: Address, owner: str, id: Optional[str] = None):
        self.name: str = name
        self.address: Address = address
        self.owner: str = owner
        super(Shop, self).__init__(id)

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'address': self.address.to_db_object(),
            'owner': ObjectId(self.owner),
        }

    def to_response(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address.to_response(),
            'owner': self.owner
        }


class ShopHandler(AbstractHandler):

    @inject
    def __init__(self, dao: ShopsDAO, shop_owner_handler: ShopOwnerHandler, address_handler: AddressHandler):
        self.dao: ShopsDAO = dao
        self.shop_owner_handler: ShopOwnerHandler = shop_owner_handler
        self.address_handler: AddressHandler = address_handler
        super().__init__(Shop, dao)

    def from_db_object(self, db_object: Dict[str, Any]) -> Shop:
        return Shop(
            name=db_object['name'],
            address=self.address_handler.from_db_object(db_object['address']),
            owner=str(db_object['owner']),
            id=str(db_object['_id'])
        )

    def create_shop(self, name: str, street: str, zip: str, country: str, session_id: str) -> str:
        shop_owner_id = self.shop_owner_handler.get_user_id_from_session_id(session_id)
        address = self.address_handler(street, zip, country)
        shop = Shop(
            name=name,
            address=address,
            owner=shop_owner_id
        )
        id = self.dao.store_one(shop.to_db_object())
        return id

    def get_shops(self) -> List[Dict[str, Any]]:
        return [self.from_db_object(db_obj).to_response() for db_obj in self.dao.get_all()]
