from pymongo.database import Database

from dao.abstract_dao import AbstractDAO


class ShopsDAO(AbstractDAO):

    def __init__(self, db: Database):
        super(ShopsDAO, self).__init__(db, 'Shops')
