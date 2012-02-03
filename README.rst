=============
python-google-places
=============

.. _introduction:

**python-google-places** provides a simple wrapper around the experimental
Google Places API.


Installation
============

.. _installation:
sudo pip install https://github.com/slimkrazy/python-google-places/zipball/master

OR

Download source and then:
python setup.py install


Prerequisites
============

.. _prerequisites:
A Google API key with Places activated against it. Please check the Google API
console, here: http://code.google.com/apis/console


Usage
=====

.. _usage:
Code is easier to understand than words, so::

    from googleplaces import GooglePlaces, types

    YOUR_API_KEY = 'AIzaSyAiFpFd85eMtfbvmVNEYuNds5TEF9FjIPI'

    query_result = GooglePlaces(YOUR_API_KEY).query(
            location='London, England', keyword='Fish and Chips',
            radius=20000, types=[types.TYPE_FOOD])

    if query_result.has_attributions:
        print query_result.html_attributions


    for place in query_result.places:
        # Returned places from a query are place summaries.
        print place.name
        print place.geo_location
        print place.reference

        # The following method has to make a further API call.
        place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        print place.details # A dict matching the JSON response from Google.
        print place.local_phone_number
        print place.international_phone_number
        print place.website
        print place.url



Known Issues
=========
Support for adding and deleting pending.


Reference
=========
googleplaces.geocode_location(location, sensor=False)


googleplaces.GooglePlacesError
googleplaces.GooglePlacesAttributeError


googleplaces.GooglePlaces
  query()
    Returns googleplaces.GooglePlacesSearchResult

  get_place(reference)
    Returns a detailed instance of googleplaces.Place

  checkin(reference, sensor=False)
    Checks in an anonynomous user in to the Place that matches the reference.


googleplaces.GooglePlacesSearchResult
  places
    A list of summary googleplaces.Place instances.

  has_attributions()
    Returns a flag indicating if the search result has html attributions that
    must be displayed.

  html_attributions()
    Returns a List of String html attributions that must be displayed along with
    the search results.

googleplaces.Place
  reference
    Returns a unique identifier for the Place that can be used to fetch full
    details about it. It is recommended that stored references for Places be
    regularly updated. A Place may have many valid reference tokens.

  id
    Returns a unique stable identifier denoting this Place. This identifier
    may not be used to retrieve information about this Place, but can be used to consolidate data about this Place, and to verify the identity of a Place across separate searches

  icon
    contains the URL of a suggested icon which may be displayed to the user when
    indicating this result on a map.

  types
    Returns a List of feature types describing the given result.

  geo_location
    Returns the geocoded latitude,longitude value for this Place.

  name
    Returns the human-readable name for the Place.

  vicinity
    Returns a feature name of a nearby location. Often this feature refers to a
    street or neighborhood.

  rating
    Returns the Place's rating, from 0.0 to 5.0, based on user reviews.

  details
    Returns a Dict representing the full response from the details API request.
    This property will raise a googleplaces.GooglePlacesAttributeError if it is
    referenced prior to get_details()

  formatted_address
    Returns a string containing the human-readable address of this place. Often
    this address is equivalent to the "postal address".
    This property will raise a googleplaces.GooglePlacesAttributeError if it is
    referenced prior to get_details()

  local_phone_number
    Returns the Place's phone number in its local format.
    This property will raise a googleplaces.GooglePlacesAttributeError if it is
    referenced prior to get_details()

  international_phone_number
    Returns the Place's phone number in international format. International
    format includes the country code, and is prefixed with the plus (+) sign.
    This property will raise a googleplaces.GooglePlacesAttributeError if it is
    referenced prior to get_details()

  website
    Returns the authoritative website for this Place, such as a business'
    homepage.

  url
    Returns the official Google Place Page URL of this Place.

  has_attributions
    Returns a flag indicating if the search result has html attributions that
    must be displayed. along side the detailed query result.

  html_attributions
    Returns a List of String html attributions that must be displayed along with
    the detailed query result.

  checkin()
    Checks in an anonynomous user in.

  get_details()
    Retrieves full information on the place matching the reference.

