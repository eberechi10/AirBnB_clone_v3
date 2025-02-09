#!/usr/bin/python3
""" module containing index for the API."""

from flask import jsonify

from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ gets the JSON """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """gets number of each objects base on type """

    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),

        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
