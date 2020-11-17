from typing import Any, Dict, List

from bson import ObjectId
from pymongo.database import Database

from dao.abstract_dao import AbstractDAO


class ShopsDAO(AbstractDAO):

    def __init__(self, db: Database):
        super(ShopsDAO, self).__init__(db, 'Shops')

    def get_by_shop_owner_id(self, shop_owner_id: str) -> List[Dict[str, Any]]:
        return list(self.collection.find({'owner': ObjectId(shop_owner_id)}))
