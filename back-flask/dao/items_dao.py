from typing import Optional, Dict, Any, List

from bson import ObjectId
from pymongo.database import Database

from dao.abstract_dao import AbstractDAO


class ItemsDAO(AbstractDAO):

    def __init__(self, db: Database):
        super(ItemsDAO, self).__init__(db, 'Items')

    def get_items_by_shop_and_category(self, shop_id: Optional[str], category: Optional[str]) -> List[Dict[str, Any]]:
        query = {}
        if shop_id is not None:
            query['shop'] = ObjectId(shop_id)
        if category is not None:
            query['category'] = category
        return list(self.collection.find(query))


