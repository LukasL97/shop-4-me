from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from dao.abstract_dao import AbstractDAO
from model.exception import ObjectIdNotFoundError


class AbstractModel(ABC):

    def __init__(self, id: Optional[str]):
        self.id = id

    @classmethod
    @abstractmethod
    def get_dao(cls) -> AbstractDAO:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_db_object(cls, db_object: Dict[str, Any]) -> AbstractModel:
        raise NotImplementedError

    @abstractmethod
    def to_db_object(self) -> Dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def get_from_id(cls, id: str) -> AbstractModel:
        db_object = cls.get_dao().get_from_id(id)
        if db_object is not None:
            return cls.from_db_object(db_object)
        else:
            raise ObjectIdNotFoundError(id)
