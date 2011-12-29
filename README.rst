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


Usage
=====

.. _flavours:
Code is easier to understand than words, so::

    from googleplaces import GooglePlaces, types

    YOUR_API_KEY = 'AIzaSyAiFpFd85eMtfbvmVNEYuNds5TEF9FjIPI'

    query_result = GooglePlaces(YOUR_API_KEY).query(
            location='London, England', keyword='Fish and Chips',
            radius=20000, types=[types.TYPE_FOOD])

    if query_result.has_attributions:
        print query_result.html_attributions

    for place in query_result.places:
        print place.name
        print place.geo_location
        print place.reference


Reference
=========
TODO