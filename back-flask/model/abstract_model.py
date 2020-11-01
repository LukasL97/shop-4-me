from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Type

from injector import inject

from dao.abstract_dao import AbstractDAO
from model.exception import ObjectIdNotFoundError


class AbstractModel(ABC):
    ''' Base class for application logic objects '''

    def __init__(self, id: Optional[str]):
        self.id = id

    @abstractmethod
    def to_db_object(self) -> Dict[str, Any]:
        raise NotImplementedError


class AbstractHandler(ABC):
    ''' Base handler class for application logic objects '''

    @inject
    def __init__(self, model_cls: Type[AbstractModel], dao: AbstractDAO):
        self.model_cls = model_cls
        self.dao = dao

    @abstractmethod
    def from_db_object(self, db_object: Dict[str, Any]) -> AbstractModel:
        raise NotImplementedError

    def get_from_id(self, id: str) -> AbstractModel:
        db_object = self.dao.get_from_id(id)
        if db_object is not None:
            return self.from_db_object(db_object)
        else:
            raise ObjectIdNotFoundError(id, self.model_cls.__name__)
