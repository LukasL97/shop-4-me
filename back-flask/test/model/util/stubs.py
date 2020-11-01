from typing import Tuple

from model.exception import UnexpectedNumberOfLocationsForAddressError
from model.location.geocoding import AddressLocator


class AddressLocatorStub(AddressLocator):

    valid_street_1 = 'Some Street 42'
    valid_zip_1 = '1337'
    valid_country_1 = 'Funland'
    lat_1 = 42.0
    lng_1 = 13.37

    valid_street_2 = 'Other Street 24'
    valid_zip_2 = '12345'
    valid_country_2 = 'Otherland'
    lat_2 = 23.0
    lng_2 = 32.0

    def __init__(self):
        pass

    def get_coordinates(self, street: str, zip: str, country: str) -> Tuple[float, float]:
        if street == self.valid_street_1 and zip == self.valid_zip_1 and country == self.valid_country_1:
            return self.lat_1, self.lng_1
        if street == self.valid_street_2 and zip == self.valid_zip_2 and country == self.valid_country_2:
            return self.lat_2, self.lng_2
        raise UnexpectedNumberOfLocationsForAddressError(0, street + ', ' + zip + ', ' + country)
