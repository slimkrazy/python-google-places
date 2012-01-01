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


googleplaces.GooglePlacesSearchResult
  places
    A list of summary googleplaces.Place instances.

  has_attributions()

  html_attributions()


googleplaces.Place
  reference
  id
  icon
  types
  geo_location
  name
  vicinity
  rating

  details
  formatted_address
  local_phone_number
  international_phone_number
  website
  url

  has_attributions()
  html_attributions()
  checkin()
  get_details()

