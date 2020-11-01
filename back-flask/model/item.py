from __future__ import annotations

from typing import Optional, Dict, Any, List

from bson import ObjectId
from injector import inject

from dao.items_dao import ItemsDAO
from model.abstract_model import AbstractModel, AbstractHandler
from model.exception import UserSessionIdNotFoundError
from model.product_details import ProductDetails
from model.user import ShopOwnerHandler


class Item(AbstractModel):

    def __init__(self, name: str, price: float, category: str, shop: str, details: Optional[ProductDetails], id: Optional[str] = None):
        self.name: str = name
        self.price: float = price
        self.category: str = category
        self.shop: str = shop
        self.details: ProductDetails = details
        super(Item, self).__init__(id)

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'shop': ObjectId(self.shop),
            'details': self.details.to_db_object()
        }

    def to_response(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'shop': self.shop,
            'details': self.details.to_response()
        }


class ItemHandler(AbstractHandler):

    @inject
    def __init__(self, dao: ItemsDAO, shop_owner_handler: ShopOwnerHandler):
        self.dao = dao
        self.shop_owner_handler = shop_owner_handler
        super().__init__(Item, dao)

    def from_db_object(self, db_object: Dict[str, Any]) -> Item:
        return Item(
            name=db_object['name'],
            price=db_object['price'],
            category=db_object['category'],
            shop=str(db_object['shop']),
            details=ProductDetails.from_db_object(db_object['details']),
            id=str(db_object['_id'])
        )

    def get_items_by_shop_and_category(self, shop_id: Optional[str], category: Optional[str]) -> List[Dict[str, Any]]:
        items = [self.from_db_object(db_obj) for db_obj in self.dao.get_items_by_shop_and_category(shop_id, category)]
        return [item.to_response() for item in items]

    def validate(self, item: Item, session_id: str) -> None:
        if session_id not in self.shop_owner_handler.active_user_sessions:
            raise UserSessionIdNotFoundError
        # elif False:
        #     # TODO: ensure that shop is actually in database
        #     raise ShopDoesNotExistError
        # elif False:
        #     # TODO: ensure that shop is owned by correct ShopOwner
        #     raise UnauthorizedAccessError

    def add_item(self, name: str, price: float, category: str, shop: str, description: str, attributes: Dict[str, Any], session_id: str) -> str:
        item = Item(
            name=name,
            price=price,
            category=category,
            shop=shop,
            details=ProductDetails(description, attributes)
        )
        self.validate(item, session_id)
        id = self.dao.store_one(item.to_db_object())
        return id
