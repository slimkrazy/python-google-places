"""
Unit tests for google places.

@author: sam@slimkrazy.com
"""

from random import randint
import unittest

from googleplaces import GooglePlaces, GooglePlacesSearchResult
from testfixtures import PLACES_QUERY_RESPONSE

DUMMY_API_KEY = 'foobarbaz'


class Test(unittest.TestCase):

    def setUp(self):
        self._places_instance = GooglePlaces(DUMMY_API_KEY)

    def tearDown(self):
        self._places_instance = None


    def testSuccessfulResponse(self):
        query_result = GooglePlacesSearchResult(
                self._places_instance,
                PLACES_QUERY_RESPONSE)
        self.assertEqual(5, len(query_result.places),
                         'Place count is incorrect.')
        place_index = randint(0, len(query_result.places))
        place = query_result.places[place_index]
        response_place_entity = PLACES_QUERY_RESPONSE['results'][place_index]
        self.assertEqual(place.id, response_place_entity.get('id'),
                         'ID value is incorrect.')
        self.assertEqual(
                         place.reference,
                         response_place_entity.get('reference'),
                         'Reference value is incorrect.')
        self.assertEqual(place.name, response_place_entity.get('name'),
                         'Name value is incorrect.')
        self.assertEqual(place.vicinity, response_place_entity.get('vicinity'),
                         'Vicinity value is incorrect.')
        self.assertEqual(
                place.geo_location,
                response_place_entity['geometry']['location'],
                'Geo-location value is incorrect.')
        self.assertEqual(place.rating, response_place_entity.get('rating'),
                         'Rating value is incorrect.')
        #TODO: Testing of data pulled by the details API - Requires mocking.


if __name__ == "__main__":
    unittest.main()