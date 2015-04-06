"""
Unit tests for google places.

@author: sam@slimkrazy.com
"""

from random import randint
import unittest
import warnings

from googleplaces import (
    GooglePlaces,
    GooglePlacesSearchResult,
    GoogleAutocompleteSearchResult,
)
from testfixtures import PLACES_QUERY_RESPONSE, AUTOCOMPLETE_QUERY_RESPONSE

DUMMY_API_KEY = 'foobarbaz'


class Test(unittest.TestCase):

    def setUp(self):
        self._places_instance = GooglePlaces(DUMMY_API_KEY)

    def tearDown(self):
        self._places_instance = None

    def testSuccessfulPlaceResponse(self):
        query_result = GooglePlacesSearchResult(
                self._places_instance,
                PLACES_QUERY_RESPONSE)

        self.assertEqual(5, len(query_result.places), 'Place count is incorrect.')
        place_index = randint(0, len(query_result.places)-1)
        place = query_result.places[place_index]
        response_place_entity = PLACES_QUERY_RESPONSE['results'][place_index]

        # make sure Place.id and Place.reference raise appropriate warnings
        with warnings.catch_warnings(record=True) as w:
            place_id = place.id
            place_reference = place.reference
            self.assertEqual(len(w), 2)
            self.assertEqual(w[0].category, FutureWarning)
            self.assertEqual(w[1].category, FutureWarning)

        self.assertEqual(place_id, response_place_entity.get('id'), 'ID value is incorrect.')
        self.assertEqual(place_reference,
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

    def testSuccessfulAutocompleteResponse(self):
        query_result = GoogleAutocompleteSearchResult(
                self._places_instance,
                AUTOCOMPLETE_QUERY_RESPONSE)

        self.assertEqual(5, len(query_result.predictions), 'Prediction count is incorrect.')
        prediction_index = randint(0, len(query_result.predictions)-1)
        prediction = query_result.predictions[prediction_index]
        response_prediction_entity = AUTOCOMPLETE_QUERY_RESPONSE['predictions'][prediction_index]
        self.assertEqual(prediction.id, response_prediction_entity.get('id'), 'ID value is incorrect.')
        self.assertEqual(
                         prediction.place_id,
                         response_prediction_entity.get('place_id'),
                         'Place ID value is incorrect.')
        self.assertEqual(
                         prediction.reference,
                         response_prediction_entity.get('reference'),
                         'Reference value is incorrect.')
        self.assertEqual(prediction.description,
                         response_prediction_entity.get('description'),
                         'Description value is incorrect.')
        self.assertEqual(prediction.types,
                         response_prediction_entity.get('types'),
                         'Types value is incorrect.')


if __name__ == "__main__":
    unittest.main()
