from __future__ import annotations

from typing import Optional, Dict, Any, List

from bson import ObjectId

from dao.items_dao import ItemsDAO
from db import db
from model.abstract_model import AbstractModel
from model.exception import UserSessionIdNotFoundError
from model.user import ShopOwner


class Item(AbstractModel):

    def __init__(self, name: str, price: float, category: str, shop: str, id: Optional[str] = None):
        self.name: str = name
        self.price: float = price
        self.category: str = category
        self.shop: str = shop
        super(Item, self).__init__(id)

    @classmethod
    def get_dao(cls) -> ItemsDAO:
        return ItemsDAO(db)

    @classmethod
    def from_db_object(cls, db_object: Dict[str, Any]) -> Item:
        return Item(
            name=db_object['name'],
            price=db_object['price'],
            category=db_object['category'],
            shop=str(db_object['shop']),
            id=str(db_object['_id'])
        )

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'shop': ObjectId(self.shop)
        }

    def to_response(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'shop': self.shop
        }

    def validate(self, session_id: str) -> None:
        if session_id not in ShopOwner.active_user_sessions:
            raise UserSessionIdNotFoundError
        # elif False:
        #     # TODO: ensure that shop is actually in database
        #     raise ShopDoesNotExistError
        # elif False:
        #     # TODO: ensure that shop is owned by correct ShopOwner
        #     raise UnauthorizedAccessError


    @classmethod
    def get_items_by_shop_and_category(cls, shop_id: Optional[str], category: Optional[str]) -> List[Dict[str, Any]]:
        items = [Item.from_db_object(db_obj) for db_obj in cls.get_dao().get_items_by_shop_and_category(shop_id, category)]
        return [item.to_response() for item in items]

    @classmethod
    def add_item(cls, name: str, price: float, category: str, shop: str, session_id: str) -> str:
        item = Item(
            name=name,
            price=price,
            category=category,
            shop=shop
        )
        item.validate(session_id)
        id = cls.get_dao().store_one(item.to_db_object())
        return id
