from __future__ import annotations

from typing import Any, Dict, Optional

from geopy.distance import distance
from injector import inject

from model.location.geocoding import AddressLocator


class Address(object):

    def __init__(self, street: str, zip: str, country: str, lat: float, lng: float):
        self.street = street
        self.zip = zip
        self.country = country
        self.lat = lat
        self.lng = lng

    def to_db_object(self) -> Dict[str, Any]:
        return {
            'street': self.street,
            'zip': self.zip,
            'country': self.country,
            'coordinates': {
                'lat': self.lat,
                'lng': self.lng
            }
        }

    def to_response(self) -> Dict[str, Any]:
        return self.to_db_object()

    def __eq__(self, other: Address) -> bool:
        return self.street == other.street and self.zip == other.zip and self.country == other.country and self.lat == other.lat and self.lng == other.lng

    def distance_to_coordinates(self, lat: float, lng: float) -> float:
        return distance(
            (self.lat, self.lng),
            (lat, lng)
        ).kilometers


class AddressHandler(object):

    @inject
    def __init__(self, address_locator: AddressLocator):
        self.address_locator: AddressLocator = address_locator

    def __call__(self, street: str, zip: str, country: str, lat: Optional[float] = None, lng: Optional[float] = None) -> Address:
        if lat is None or lng is None:
            lat, lng = self.address_locator.get_coordinates(street, zip, country)
        return Address(street, zip, country, lat, lng)

    def from_db_object(self, db_object: Dict[str, Any]) -> Address:
        return Address(
            db_object['street'],
            db_object['zip'],
            db_object['country'],
            db_object['coordinates']['lat'],
            db_object['coordinates']['lng']
        )
