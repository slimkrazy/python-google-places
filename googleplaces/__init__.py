"""
A simple wrapper around the 'experimental' Google Places API, documented
here: http://code.google.com/apis/maps/documentation/places/. This library
also makes use of the v3 Maps API for geocoding.

Prerequisites: A Google API key with Places activated against it. Please
check the Google API console, here: http://code.google.com/apis/console

NOTE: Please ensure that you read the Google terms of service (labelled 'Limits
and Requirements' on the documentation url) prior to using this library in a
production environment.

@author: sam@slimkrazy.com
"""
from __future__ import absolute_import

import cgi
from decimal import Decimal
try:
    import json
except ImportError:
    import simplejson as json

try:
    import six
    from six.moves import urllib
except ImportError:
    pass

import warnings

from . import lang
from . import ranking


__all__ = ['GooglePlaces', 'GooglePlacesError', 'GooglePlacesAttributeError',
           'geocode_location']
__version__ = '1.4.1'
__author__ = 'Samuel Adu'
__email__ = 'sam@slimkrazy.com'


class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result


def _fetch_remote(service_url, params=None, use_http_post=False):
    if not params:
        params = {}

    encoded_data = {}
    for k, v in params.items():
        if isinstance(v, six.string_types):
            v = v.encode('utf-8')
        encoded_data[k] = v
    encoded_data = urllib.parse.urlencode(encoded_data)

    if not use_http_post:
        query_url = (service_url if service_url.endswith('?') else
                     '%s?' % service_url)
        request_url = query_url + encoded_data
        request = urllib.request.Request(request_url)
    else:
        request_url = service_url
        request = urllib.request.Request(service_url, data=encoded_data)
    return (request_url, urllib.request.urlopen(request))

def _fetch_remote_json(service_url, params=None, use_http_post=False):
    """Retrieves a JSON object from a URL."""
    if not params:
        params = {}

    request_url, response = _fetch_remote(service_url, params, use_http_post)
    if six.PY3:
        str_response = response.read().decode('utf-8')
        return (request_url, json.loads(str_response, parse_float=Decimal))
    return (request_url, json.load(response, parse_float=Decimal))

def _fetch_remote_file(service_url, params=None, use_http_post=False):
    """Retrieves a file from a URL.

    Returns a tuple (mimetype, filename, data)
    """
    if not params:
        params = {}

    request_url, response = _fetch_remote(service_url, params, use_http_post)
    dummy, params = cgi.parse_header(
            response.headers.get('Content-Disposition', ''))
    fn = params['filename']

    return (response.headers.get('content-type'),
            fn, response.read(), response.geturl())

def geocode_location(location, sensor=False, api_key=None):
    """Converts a human-readable location to lat-lng.

    Returns a dict with lat and lng keys.

    keyword arguments:
    location -- A human-readable location, e.g 'London, England'
    sensor   -- Boolean flag denoting if the location came from a device using
                its' location sensor (default False)
    api_key  -- A valid Google Places API key. 

    raises:
    GooglePlacesError -- if the geocoder fails to find a location.
    """
    params = {'address': location, 'sensor': str(sensor).lower()}
    if api_key is not None:
        params['key'] = api_key
    url, geo_response = _fetch_remote_json(
            GooglePlaces.GEOCODE_API_URL, params)
    _validate_response(url, geo_response)
    if geo_response['status'] == GooglePlaces.RESPONSE_STATUS_ZERO_RESULTS:
        error_detail = ('Lat/Lng for location \'%s\' can\'t be determined.' %
                        location)
        raise GooglePlacesError(error_detail)
    return geo_response['results'][0]['geometry']['location']

def _get_place_details(place_id, api_key, sensor=False,
                       language=lang.ENGLISH):
    """Gets a detailed place response.

    keyword arguments:
    place_id -- The unique identifier for the required place.
    """
    url, detail_response = _fetch_remote_json(GooglePlaces.DETAIL_API_URL,
                                              {'placeid': place_id,
                                               'sensor': str(sensor).lower(),
                                               'key': api_key,
                                               'language': language})
    _validate_response(url, detail_response)
    return detail_response['result']

def _get_place_photo(photoreference, api_key, maxheight=None, maxwidth=None,
                       sensor=False):
    """Gets a place's photo by reference.
    See detailed documentation at https://developers.google.com/places/documentation/photos

    Arguments:
    photoreference -- The unique Google reference for the required photo.

    Keyword arguments:
    maxheight -- The maximum desired photo height in pixels
    maxwidth -- The maximum desired photo width in pixels

    You must specify one of this keyword arguments. Acceptable value is an
    integer between 1 and 1600.
    """

    params = {'photoreference': photoreference,
              'sensor': str(sensor).lower(),
              'key': api_key}

    if maxheight:
        params['maxheight'] = maxheight

    if maxwidth:
        params['maxwidth'] = maxwidth

    return _fetch_remote_file(GooglePlaces.PHOTO_API_URL, params)

def _validate_response(url, response):
    """Validates that the response from Google was successful."""
    if response['status'] not in [GooglePlaces.RESPONSE_STATUS_OK,
                                  GooglePlaces.RESPONSE_STATUS_ZERO_RESULTS]:
        error_detail = ('Request to URL %s failed with response code: %s' %
                        (url, response['status']))
        raise GooglePlacesError(error_detail)


class GooglePlacesError(Exception):
    pass


class GooglePlacesAttributeError(AttributeError):
    """Exception thrown when a detailed property is unavailable.

    A search query from the places API returns only a summary of the Place.
    in order to get full details, a further API call must be made using
    the place_id. This exception will be thrown when a property made
    available by only the detailed API call is looked up against the summary
    object.

    An explicit call to get_details() must be made on the summary object in
    order to convert a summary object to a detailed object.
    """
    # I could spend forever muling between this design decision and creating
    # a PlaceSummary object as well as a Place object. I'm leaning towards this
    # method in order to keep the API as simple as possible.
    pass


class GooglePlaces(object):
    """A wrapper around the Google Places Query API."""

    BASE_URL = 'https://maps.googleapis.com/maps/api'
    PLACE_URL = BASE_URL + '/place'
    GEOCODE_API_URL = BASE_URL + '/geocode/json?'
    RADAR_SEARCH_API_URL = PLACE_URL + '/radarsearch/json?'
    NEARBY_SEARCH_API_URL = PLACE_URL + '/nearbysearch/json?'
    TEXT_SEARCH_API_URL = PLACE_URL + '/textsearch/json?'
    AUTOCOMPLETE_API_URL = PLACE_URL + '/autocomplete/json?'
    DETAIL_API_URL = PLACE_URL + '/details/json?'
    CHECKIN_API_URL = PLACE_URL + '/check-in/json?sensor=%s&key=%s'
    ADD_API_URL = PLACE_URL + '/add/json?sensor=%s&key=%s'
    DELETE_API_URL = PLACE_URL + '/delete/json?sensor=%s&key=%s'
    PHOTO_API_URL = PLACE_URL + '/photo?'

    MAXIMUM_SEARCH_RADIUS = 50000
    RESPONSE_STATUS_OK = 'OK'
    RESPONSE_STATUS_ZERO_RESULTS = 'ZERO_RESULTS'

    def __init__(self, api_key):
        self._api_key = api_key
        self._sensor = False
        self._request_params = None

    def query(self, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('always')
            warnings.warn('The query API is deprecated. Please use nearby_search.',
                          DeprecationWarning, stacklevel=2)
        return self.nearby_search(**kwargs)

    def nearby_search(self, language=lang.ENGLISH, keyword=None, location=None,
               lat_lng=None, name=None, radius=3200, rankby=ranking.PROMINENCE,
               sensor=False, type=None, types=[], pagetoken=None):
        """Perform a nearby search using the Google Places API.

        One of either location, lat_lng or pagetoken are required, the rest of 
        the keyword arguments are optional.

        keyword arguments:
        keyword  -- A term to be matched against all available fields, including
                    but not limited to name, type, and address (default None)
        location -- A human readable location, e.g 'London, England'
                    (default None)
        language -- The language code, indicating in which language the
                    results should be returned, if possible. (default lang.ENGLISH)
        lat_lng  -- A dict containing the following keys: lat, lng
                    (default None)
        name     -- A term to be matched against the names of the Places.
                    Results will be restricted to those containing the passed
                    name value. (default None)
        radius   -- The radius (in meters) around the location/lat_lng to
                    restrict the search to. The maximum is 50000 meters.
                    (default 3200)
        rankby   -- Specifies the order in which results are listed :
                    ranking.PROMINENCE (default) or ranking.DISTANCE
                    (imply no radius argument).
        sensor   -- Indicates whether or not the Place request came from a
                    device using a location sensor (default False).
        type     -- Optional type param used to indicate place category.
        types    -- An optional list of types, restricting the results to
                    Places (default []). If there is only one item the request
                    will be send as type param.
        pagetoken-- Optional parameter to force the search result to return the next
                    20 results from a previously run search. Setting this parameter 
                    will execute a search with the same parameters used previously. 
                    (default None)
        """
        if location is None and lat_lng is None and pagetoken is None:
            raise ValueError('One of location, lat_lng or pagetoken must be passed in.')
        if rankby == 'distance':
            # As per API docs rankby == distance:
            #  One or more of keyword, name, or types is required.
            if keyword is None and types == [] and name is None:
                raise ValueError('When rankby = googleplaces.ranking.DISTANCE, ' +
                                 'name, keyword or types kwargs ' +
                                 'must be specified.')
        self._sensor = sensor
        radius = (radius if radius <= GooglePlaces.MAXIMUM_SEARCH_RADIUS
                  else GooglePlaces.MAXIMUM_SEARCH_RADIUS)
        lat_lng_str = self._generate_lat_lng_string(lat_lng, location)
        self._request_params = {'location': lat_lng_str}
        if rankby == 'prominence':
            self._request_params['radius'] = radius
        else:
            self._request_params['rankby'] = rankby
        if type:
            self._request_params['type'] = type
        elif types:
            if len(types) == 1:
                self._request_params['type'] = types[0]
            elif len(types) > 1:
                self._request_params['types'] = '|'.join(types)
        if keyword is not None:
            self._request_params['keyword'] = keyword
        if name is not None:
            self._request_params['name'] = name
        if pagetoken is not None:
            self._request_params['pagetoken'] = pagetoken
        if language is not None:
            self._request_params['language'] = language
        self._add_required_param_keys()
        url, places_response = _fetch_remote_json(
                GooglePlaces.NEARBY_SEARCH_API_URL, self._request_params)
        _validate_response(url, places_response)
        return GooglePlacesSearchResult(self, places_response)

    def text_search(self, query=None, language=lang.ENGLISH, lat_lng=None,
                    radius=3200, type=None, types=[], location=None, pagetoken=None):
        """Perform a text search using the Google Places API.

        Only the one of the query or pagetoken kwargs are required, the rest of the 
        keyword arguments are optional.

        keyword arguments:
        lat_lng  -- A dict containing the following keys: lat, lng
                    (default None)
        location -- A human readable location, e.g 'London, England'
                    (default None)
        pagetoken-- Optional parameter to force the search result to return the next
                    20 results from a previously run search. Setting this parameter 
                    will execute a search with the same parameters used previously. 
                    (default None)
        radius   -- The radius (in meters) around the location/lat_lng to
                    restrict the search to. The maximum is 50000 meters.
                    (default 3200)
        query    -- The text string on which to search, for example:
                    "Restaurant in New York".
        type     -- Optional type param used to indicate place category.
        types    -- An optional list of types, restricting the results to
                    Places (default []). If there is only one item the request
                    will be send as type param.
        """
        self._request_params = {'query': query}
        if lat_lng is not None or location is not None:
            lat_lng_str = self._generate_lat_lng_string(lat_lng, location)
            self._request_params['location'] = lat_lng_str
        self._request_params['radius'] = radius
        if type:
            self._request_params['type'] = type
        elif types:
            if len(types) == 1:
                self._request_params['type'] = types[0]
            elif len(types) > 1:
                self._request_params['types'] = '|'.join(types)
        if language is not None:
            self._request_params['language'] = language
        if pagetoken is not None:
            self._request_params['pagetoken'] = pagetoken
        self._add_required_param_keys()
        url, places_response = _fetch_remote_json(
                GooglePlaces.TEXT_SEARCH_API_URL, self._request_params)
        _validate_response(url, places_response)
        return GooglePlacesSearchResult(self, places_response)

    def autocomplete(self, input, lat_lng=None, location=None, radius=3200,
                     language=lang.ENGLISH, types=None, components=[]):
        """
        Perform an autocomplete search using the Google Places API.

        Only the input kwarg is required, the rest of the keyword arguments
        are optional.

        keyword arguments:
        input    -- The text string on which to search, for example:
                    "Hattie B's".
        lat_lng  -- A dict containing the following keys: lat, lng
                    (default None)
        location -- A human readable location, e.g 'London, England'
                    (default None)
        radius   -- The radius (in meters) around the location to which the
                    search is to be restricted. The maximum is 50000 meters.
                    (default 3200)
        language -- The language code, indicating in which language the
                    results should be returned, if possible. (default lang.ENGLISH)
        types    -- A type to search against. See `types.py` "autocomplete types"
                    for complete list
                    https://developers.google.com/places/documentation/autocomplete#place_types.
        components -- An optional grouping of places to which you would
                    like to restrict your results. An array containing one or
                    more tuples of:
                    * country: matches a country name or a two letter ISO 3166-1 country code.
                    eg: [('country','US')]
        """
        self._request_params = {'input': input}
        if lat_lng is not None or location is not None:
            lat_lng_str = self._generate_lat_lng_string(lat_lng, location)
            self._request_params['location'] = lat_lng_str
        self._request_params['radius'] = radius
        if types:
            self._request_params['types'] = types
        if len(components) > 0:
            self._request_params['components'] = '|'.join(['{}:{}'.format(
                                                     c[0],c[1]) for c in components])
        if language is not None:
            self._request_params['language'] = language
        self._add_required_param_keys()
        url, places_response = _fetch_remote_json(
                GooglePlaces.AUTOCOMPLETE_API_URL, self._request_params)
        _validate_response(url, places_response)
        return GoogleAutocompleteSearchResult(self, places_response)

    def radar_search(self, sensor=False, keyword=None, name=None,
                     language=lang.ENGLISH, lat_lng=None, opennow=False,
                     radius=3200, type=None, types=[], location=None):
        """Perform a radar search using the Google Places API.

        One of lat_lng or location are required, the rest of the keyword
        arguments are optional.

        keyword arguments:
        keyword  -- A term to be matched against all available fields, including
                    but not limited to name, type, and address (default None)
        name     -- A term to be matched against the names of Places. Results will
                    be restricted to those containing the passed name value.
        language -- The language code, indicating in which language the
                    results should be returned, if possible. (default lang.ENGLISH)
        lat_lng  -- A dict containing the following keys: lat, lng
                    (default None)
        location -- A human readable location, e.g 'London, England'
                    (default None)
        radius   -- The radius (in meters) around the location/lat_lng to
                    restrict the search to. The maximum is 50000 meters.
                    (default 3200)
        opennow  -- Returns only those Places that are open for business at the time
                    the query is sent. (default False)
        sensor   -- Indicates whether or not the Place request came from a
                    device using a location sensor (default False).
        type     -- Optional type param used to indicate place category
        types    -- An optional list of types, restricting the results to
                    Places (default []). If there is only one item the request
                    will be send as type param
        """
        if keyword is None and name is None and len(types) is 0:
            raise ValueError('One of keyword, name or types must be supplied.')
        if location is None and lat_lng is None:
            raise ValueError('One of location or lat_lng must be passed in.')
        try:
            radius = int(radius)
        except:
            raise ValueError('radius must be passed supplied as an integer.')
        if sensor not in [True, False]:
            raise ValueError('sensor must be passed in as a boolean value.')

        self._request_params = {'radius': radius}
        self._sensor = sensor
        self._request_params['location'] = self._generate_lat_lng_string(
                lat_lng, location)
        if keyword is not None:
            self._request_params['keyword'] = keyword
        if name is not None:
            self._request_params['name'] = name
        if type:
            self._request_params['type'] = type
        elif types:
            if len(types) == 1:
                self._request_params['type'] = types[0]
            elif len(types) > 1:
                self._request_params['types'] = '|'.join(types)
        if language is not None:
            self._request_params['language'] = language
        if opennow is True:
            self._request_params['opennow'] = 'true'
        self._add_required_param_keys()
        url, places_response = _fetch_remote_json(
                GooglePlaces.RADAR_SEARCH_API_URL, self._request_params)
        _validate_response(url, places_response)
        return GooglePlacesSearchResult(self, places_response)

    def checkin(self, place_id, sensor=False):
        """Checks in a user to a place.

        keyword arguments:
        place_id  -- The unique Google identifier for the relevant place.
        sensor    -- Boolean flag denoting if the location came from a
                     device using its location sensor (default False).
        """
        data = {'placeid': place_id}
        url, checkin_response = _fetch_remote_json(
                GooglePlaces.CHECKIN_API_URL % (str(sensor).lower(),
                        self.api_key), json.dumps(data), use_http_post=True)
        _validate_response(url, checkin_response)

    def get_place(self, place_id, sensor=False, language=lang.ENGLISH):
        """Gets a detailed place object.

        keyword arguments:
        place_id -- The unique Google identifier for the required place.
        sensor    -- Boolean flag denoting if the location came from a
                     device using its' location sensor (default False).
        language -- The language code, indicating in which language the
                    results should be returned, if possible. (default lang.ENGLISH)
        """
        place_details = _get_place_details(place_id,
                self.api_key, sensor, language=language)
        return Place(self, place_details)

    def add_place(self, **kwargs):
        """Adds a place to the Google Places database.

        On a successful request, this method will return a dict containing
        the the new Place's place_id and id in keys 'place_id' and 'id'
        respectively.

        keyword arguments:
        name        -- The full text name of the Place. Limited to 255
                       characters.
        lat_lng     -- A dict containing the following keys: lat, lng.
        accuracy    -- The accuracy of the location signal on which this request
                       is based, expressed in meters.
        types       -- The category in which this Place belongs. Only one type
                       can currently be specified for a Place. A string or
                       single element list may be passed in.
        language    -- The language in which the Place's name is being reported.
                       (defaults 'en').
        sensor      -- Boolean flag denoting if the location came from a device
                       using its location sensor (default False).
        """
        required_kwargs = {'name': [str], 'lat_lng': [dict],
                           'accuracy': [int], 'types': [str, list]}
        request_params = {}
        for key in required_kwargs:
            if key not in kwargs or kwargs[key] is None:
                raise ValueError('The %s argument is required.' % key)
            expected_types = required_kwargs[key]
            type_is_valid = False
            for expected_type in expected_types:
                if isinstance(kwargs[key], expected_type):
                    type_is_valid = True
                    break
            if not type_is_valid:
                raise ValueError('Invalid value for %s' % key)
            if key is not 'lat_lng':
                request_params[key] = kwargs[key]

        if len(kwargs['name']) > 255:
            raise ValueError('The place name must not exceed 255 characters ' +
                             'in length.')
        try:
            kwargs['lat_lng']['lat']
            kwargs['lat_lng']['lng']
            request_params['location'] = kwargs['lat_lng']
        except KeyError:
            raise ValueError('Invalid keys for lat_lng.')

        request_params['language'] = (kwargs.get('language')
                if kwargs.get('language') is not None else
                lang.ENGLISH)

        sensor = (kwargs.get('sensor')
                       if kwargs.get('sensor') is not None else
                       False)

        # At some point Google might support multiple types, so this supports
        # strings and lists.
        if isinstance(kwargs['types'], str):
            request_params['types'] = [kwargs['types']]
        else:
            request_params['types'] = kwargs['types']
        url, add_response = _fetch_remote_json(
                GooglePlaces.ADD_API_URL % (str(sensor).lower(),
                self.api_key), json.dumps(request_params), use_http_post=True)
        _validate_response(url, add_response)
        return {'place_id': add_response['place_id'],
                'id': add_response['id']}

    def delete_place(self, place_id, sensor=False):
        """Deletes a place from the Google Places database.

        keyword arguments:
        place_id   -- The textual identifier that uniquely identifies this
                      Place, returned from a Place Search request.
        sensor     -- Boolean flag denoting if the location came from a device
                      using its location sensor (default False).
        """

        request_params = {'place_id': place_id}
        url, delete_response = _fetch_remote_json(
                GooglePlaces.DELETE_API_URL % (str(sensor).lower(),
                self.api_key), json.dumps(request_params), use_http_post=True)
        _validate_response(url, delete_response)

    def _add_required_param_keys(self):
        self._request_params['key'] = self.api_key
        self._request_params['sensor'] = str(self.sensor).lower()

    def _generate_lat_lng_string(self, lat_lng, location):
        try:
            return '%(lat)s,%(lng)s' % (lat_lng if lat_lng is not None
                    else geocode_location(location=location, api_key=self.api_key))
        except GooglePlacesError as e:
            raise ValueError(
                'lat_lng must be a dict with the keys, \'lat\' and \'lng\'. Cause: %s' % str(e))

    @property
    def request_params(self):
        return self._request_params

    @property
    def api_key(self):
        return self._api_key

    @property
    def sensor(self):
        return self._sensor


class GoogleAutocompleteSearchResult(object):
    """Wrapper around the Google Autocomplete API query JSON response."""

    def __init__(self, query_instance, response):
        self._response = response
        self._predictions = []
        for prediction in response['predictions']:
            self._predictions.append(Prediction(query_instance, prediction))

    @property
    def raw_response(self):
        """Returns the raw JSON response returned by the Autocomplete API."""
        return self._response

    @property
    def predictions(self):
        return self._predictions

    def __repr__(self):
        """Return a string representation stating number of predictions."""
        return '<{} with {} prediction(s)>'.format(
            self.__class__.__name__,
            len(self.predictions)
        )


class Prediction(object):
    """
    Represents a prediction from the results of a Google Places Autocomplete API query.
    """
    def __init__(self, query_instance, prediction):
        self._query_instance = query_instance
        self._description = prediction['description']
        self._id = prediction['id']
        self._matched_substrings = prediction['matched_substrings']
        self._place_id = prediction['place_id']
        self._reference = prediction['reference']
        self._terms = prediction['terms']
        self._types = prediction.get('types',[])
        if prediction.get('_description') is None:
            self._place = None
        else:
            self._place = prediction

    @property
    def description(self):
        """
        String representation of a Prediction location. Generally contains
        name, country, and elements contained in the terms property.
        """
        return self._description

    @property
    def id(self):
        """
        Returns the deprecated id property.

        This identifier may not be used to retrieve information about this
        place, but is guaranteed to be valid across sessions. It can be used
        to consolidate data about this Place, and to verify the identity of a
        Place across separate searches.

        This property is deprecated:
        https://developers.google.com/places/documentation/autocomplete#deprecation
        """
        return self._id

    @property
    def matched_substrings(self):
        """
        Returns the placement and offset of the matched strings for this search.

        A an array of dicts, each with the keys 'length' and 'offset', will be returned.
        """
        return self._matched_substrings

    @property
    def place_id(self):
        """
        Returns the unique stable identifier denoting this place.

        This identifier may be used to retrieve information about this
        place.

        This should be considered the primary identifier of a place.
        """
        return self._place_id

    @property
    def reference(self):
        """
        Returns the deprecated reference property.

        The token can be used to retrieve additional information about this
        place when invoking the getPlace method on an GooglePlaces instance.

        You can store this token and use it at any time in future to refresh
        cached data about this Place, but the same token is not guaranteed to
        be returned for any given Place across different searches.

        This property is deprecated:
        https://developers.google.com/places/documentation/autocomplete#deprecation
        """
        return self._reference

    @property
    def terms(self):
        """
        A list of terms which build up the description string

        A an array of dicts, each with the keys `offset` and `value`, will be returned.
        """
        return self._terms

    @property
    def types(self):
        """
        Returns a list of feature types describing the given result.
        """
        if self._types == '' and self.details != None and 'types' in self.details:
            self._icon = self.details['types']
        return self._types

    # The following properties require a further API call in order to be
    # available.
    @property
    def place(self):
        """
        Returns the JSON response from Google Places Detail search API.
        """
        self._validate_status()
        return self._place

    def get_details(self, language=None):
        """
        Retrieves full information on the place matching the place_id.

        Stores the response in the `place` property.
        """
        if self._place is None:
            if language is None:
                try:
                    language = self._query_instance._request_params['language']
                except KeyError:
                    language = lang.ENGLISH
            place = _get_place_details(
                    self.place_id, self._query_instance.api_key,
                    self._query_instance.sensor, language=language)
            self._place = Place(self._query_instance, place)

    def _validate_status(self):
        """
        Indicates specific properties are only available after a details call.
        """
        if self._place is None:
            error_detail = ('The attribute requested is only available after ' +
                    'an explicit call to get_details() is made.')
            raise GooglePlacesAttributeError(error_detail)

    def __repr__(self):
        """ Return a string representation with description. """
        return '<{} description="{}">'.format(self.__class__.__name__, self.description)


class GooglePlacesSearchResult(object):
    """
    Wrapper around the Google Places API query JSON response.
    """

    def __init__(self, query_instance, response):
        self._response = response
        self._places = []
        for place in response['results']:
            self._places.append(Place(query_instance, place))
        self._html_attributions = response.get('html_attributions', [])
        self._next_page_token = response.get('next_page_token', [])

    @property
    def raw_response(self):
        """
        Returns the raw JSON response returned by the Places API.
        """
        return self._response

    @property
    def places(self):
        return self._places

    @property
    def html_attributions(self):
        """Returns the HTML attributions for the specified response.

        Any returned HTML attributions MUST be displayed as-is, in accordance
        with the requirements as found in the documentation. Please see the
        module comments for links to the relevant url.
        """
        return self._html_attributions

    @property
    def next_page_token(self):
        """Returns the next page token(next_page_token)."""
        return self._next_page_token

    @property
    def has_attributions(self):
        """Returns a flag denoting if the response had any html attributions."""
        return len(self.html_attributions) > 0

    @property
    def has_next_page_token(self):
        """Returns a flag denoting if the response had a next page token."""
        return len(self.next_page_token) > 0

    def __repr__(self):
        """ Return a string representation stating the number of results."""
        return '<{} with {} result(s)>'.format(self.__class__.__name__, len(self.places))


class Place(object):
    """
    Represents a place from the results of a Google Places API query.
    """
    def __init__(self, query_instance, place_data):
        self._query_instance = query_instance
        self._place_id = place_data['place_id']
        self._id = place_data.get('id', '')
        self._reference = place_data.get('reference', '')
        self._name = place_data.get('name','')
        self._vicinity = place_data.get('vicinity', '')
        self._geo_location = place_data['geometry']['location']
        self._rating = place_data.get('rating','')
        self._types = place_data.get('types','')
        self._icon = place_data.get('icon','')
        if place_data.get('address_components') is None:
            self._details = None
        else:
            self._details = place_data

    @property
    def reference(self):
        """DEPRECATED AS OF JUNE 24, 2014. May stop being returned on June 24,
        2015. Reference: https://developers.google.com/places/documentation/search

        Returns contains a unique token for the place.

        The token can be used to retrieve additional information about this
        place when invoking the getPlace method on an GooglePlaces instance.

        You can store this token and use it at any time in future to refresh
        cached data about this Place, but the same token is not guaranteed to
        be returned for any given Place across different searches."""
        warnings.warn('The "reference" feature is deprecated and may'
                      'stop working any time after June 24, 2015.',
                      FutureWarning)
        return self._reference

    @property
    def id(self):
        """DEPRECATED AS OF JUNE 24, 2014. May stop being returned on June 24,
        2015. Reference: https://developers.google.com/places/documentation/search

        Returns the unique stable identifier denoting this place.

        This identifier may not be used to retrieve information about this
        place, but is guaranteed to be valid across sessions. It can be used
        to consolidate data about this Place, and to verify the identity of a
        Place across separate searches.
        """
        warnings.warn('The "id" feature is deprecated and may'
                      'stop working any time after June 24, 2015.',
                      FutureWarning)
        return self._id

    @property
    def place_id(self):
        """Returns the unique stable identifier denoting this place.

        This identifier may be used to retrieve information about this
        place.

        This should be considered the primary identifier of a place.
        """
        return self._place_id

    @property
    def icon(self):
        """Returns the URL of a recommended icon for display."""
        if self._icon == '' and self.details != None and 'icon' in self.details:
            self._icon = self.details['icon']
        return self._icon

    @property
    def types(self):
        """Returns a list of feature types describing the given result."""
        if self._types == '' and self.details != None and 'types' in self.details:
            self._icon = self.details['types']
        return self._types

    @property
    def geo_location(self):
        """Returns the lat lng co-ordinates of the place.

        A dict with the keys 'lat' and 'lng' will be returned.
        """
        return self._geo_location

    @property
    def name(self):
        """Returns the human-readable name of the place."""
        if self._name == '' and self.details != None and 'name' in self.details:
            self._name = self.details['name']
        return self._name

    @property
    def vicinity(self):
        """Returns a feature name of a nearby location.

        Often this feature refers to a street or neighborhood within the given
        results.
        """
        if self._vicinity == '' and self.details != None and 'vicinity' in self.details:
            self._vicinity = self.details['vicinity']
        return self._vicinity

    @property
    def rating(self):
        """Returns the Place's rating, from 0.0 to 5.0, based on user reviews.

        This method will return None for places that have no rating.
        """
        if self._rating == '' and self.details != None and 'rating' in self.details:
            self._rating = self.details['rating']
        return self._rating

    # The following properties require a further API call in order to be
    # available.
    @property
    def details(self):
        """Returns the JSON response from Google Places Detail search API."""
        self._validate_status()
        return self._details

    @property
    def formatted_address(self):
        """Returns a string containing the human-readable address of this place.

        Often this address is equivalent to the "postal address," which
        sometimes differs from country to country. (Note that some countries,
        such as the United Kingdom, do not allow distribution of complete postal
        addresses due to licensing restrictions.)
        """
        self._validate_status()
        return self.details.get('formatted_address')

    @property
    def local_phone_number(self):
        """Returns the Place's phone number in its local format."""
        self._validate_status()
        return self.details.get('formatted_phone_number')

    @property
    def international_phone_number(self):
        self._validate_status()
        return self.details.get('international_phone_number')

    @property
    def website(self):
        """Returns the authoritative website for this Place."""
        self._validate_status()
        return self.details.get('website')

    @property
    def url(self):
        """Contains the official Google Place Page URL of this establishment.

        Applications must link to or embed the Google Place page on any screen
        that shows detailed results about this Place to the user.
        """
        self._validate_status()
        return self.details.get('url')

    @property
    def html_attributions(self):
        """Returns the HTML attributions for the specified response.

        Any returned HTML attributions MUST be displayed as-is, in accordance
        with the requirements as found in the documentation. Please see the
        module comments for links to the relevant url.
        """
        self._validate_status()
        return self.details.get('html_attributions', [])

    @property
    def has_attributions(self):
        """Returns a flag denoting if the response had any html attributions."""
        return (False if self._details is None else
                len(self.html_attributions) > 0)

    def checkin(self):
        """Checks in an anonymous user in."""
        self._query_instance.checkin(self.place_id,
                                     self._query_instance.sensor)

    def get_details(self, language=None):
        """Retrieves full information on the place matching the place_id.

        Further attributes will be made available on the instance once this
        method has been invoked.

        keyword arguments:
        language -- The language code, indicating in which language the
                    results should be returned, if possible. This value defaults
                    to the language that was used to generate the
                    GooglePlacesSearchResult instance.
        """
        if self._details is None:
            if language is None:
                try:
                    language = self._query_instance._request_params['language']
                except KeyError:
                    language = lang.ENGLISH
            self._details = _get_place_details(
                    self.place_id, self._query_instance.api_key,
                    self._query_instance.sensor, language=language)

    @cached_property
    def photos(self):
        self.get_details()
        return [Photo(self._query_instance, i)
                for i in self.details.get('photos', [])]

    def _validate_status(self):
        if self._details is None:
            error_detail = ('The attribute requested is only available after ' +
                    'an explicit call to get_details() is made.')
            raise GooglePlacesAttributeError(error_detail)

    def __repr__(self):
        """ Return a string representation including the name, lat, and lng. """
        return '<{} name="{}", lat={}, lng={}>'.format(
            self.__class__.__name__,
            self.name,
            self.geo_location['lat'],
            self.geo_location['lng']
        )


class Photo(object):
    def __init__(self, query_instance, attrs):
        self._query_instance = query_instance
        self.orig_height = attrs.get('height')
        self.orig_width = attrs.get('width')
        self.html_attributions = attrs.get('html_attributions')
        self.photo_reference = attrs.get('photo_reference')

    def get(self, maxheight=None, maxwidth=None, sensor=False):
        """Fetch photo from API."""
        if not maxheight and not maxwidth:
            raise GooglePlacesError('You must specify maxheight or maxwidth!')

        result = _get_place_photo(self.photo_reference,
                                  self._query_instance.api_key,
                                  maxheight=maxheight, maxwidth=maxwidth,
                                  sensor=sensor)

        self.mimetype, self.filename, self.data, self.url = result
