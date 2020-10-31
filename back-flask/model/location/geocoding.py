from typing import Tuple

import googlemaps

from model.exception import UnexpectedNumberOfLocationsForAddressError
from paths import GOOGLE_CLOUD_PLATFORMS_API_KEY_FILE


class AddressLocator(object):

    def __init__(self):
        with open(GOOGLE_CLOUD_PLATFORMS_API_KEY_FILE, encoding='utf8', mode='r') as api_key_file:
            api_key= api_key_file.read().strip()
        self.gmaps_client: googlemaps.Client = googlemaps.Client(key=api_key)

    def get_coordinates(self, street: str, zip: str, country: str) -> Tuple[float, float]:
        ''' Returns coordinates as (latitude, longitude) '''
        address = street + ', ' + zip + ', ' + country
        api_response = self.gmaps_client.geocode(address)
        if not len(api_response) == 1:
            raise UnexpectedNumberOfLocationsForAddressError(len(api_response), address)
        location = api_response[0]['geometry']['location']
        return location['lat'], location['lng']
