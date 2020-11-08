from __future__ import annotations

from typing import Any, Dict


class Image(object):

    def __init__(self, id: str, url: str):
        self.id: str = id
        self.url: str = url

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'url': self.url
        }

    def to_response(self) -> Dict[str, Any]:
        return self.to_db_object()

    @classmethod
    def from_db_object(cls, db_object: Dict[str, Any]) -> Image:
        return cls(
            id=db_object['id'],
            url=db_object['url']
        )
