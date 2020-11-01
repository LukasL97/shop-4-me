from __future__ import annotations

from typing import Dict, Any


class ProductDetails(object):

    def __init__(self, description: str, attributes: Dict[str, Any]):
        self.description: str = description
        self.attributes: Dict[str, Any] = attributes

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'description': self.description,
            'attributes': self.attributes
        }

    def to_response(self) -> Dict[str, Any]:
        return self.to_db_object()

    @classmethod
    def from_db_object(cls, db_object: Dict[str, Any]) -> ProductDetails:
        return cls(
            description=db_object['description'],
            attributes=db_object['attributes']
        )
