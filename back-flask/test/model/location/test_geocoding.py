from unittest import TestCase

from model.exception import UnexpectedNumberOfLocationsForAddressError
from model.location.geocoding import AddressLocator


class AddressLocatorTest(TestCase):

    def test_address_locator_on_correct_input(self):
        locator = AddressLocator()
        lat, lng = locator.get_coordinates('Rosenpark 21', '65795', 'Germany')
        self.assertAlmostEqual(lat, 50.0734191)
        self.assertAlmostEqual(lng, 8.4864426)

    def test_address_locator_on_incorrect_input(self):
        locator = AddressLocator()
        with self.assertRaises(UnexpectedNumberOfLocationsForAddressError):
            locator.get_coordinates('sdkjsdfjkbsdf', 'bfasdujbisfdubisdf', 'asfbjikasdjbi')
