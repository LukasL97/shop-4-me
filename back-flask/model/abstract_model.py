from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from dao.abstract_dao import AbstractDAO


class AbstractModel(ABC):

    def __init__(self, id: Optional[str]):
        self.id = id

    @classmethod
    @abstractmethod
    def get_dao(cls) -> AbstractDAO:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_db_object(cls, db_object) -> AbstractModel:
        raise NotImplementedError

    @abstractmethod
    def to_db_object(self) -> Dict[str, Any]:
        raise NotImplementedError