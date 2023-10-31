#!/usr/bin/python3
""" module that contains places_amenities view for the API."""

from models import storage
from models import amenity

from models.amenity import Amenity
from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models.place import Place

from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """gets all Amenity objects of Place"""
    Myobj_place = storage.get(Place, place_id)
    if not Myobj_place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        Myobj = [amenity.to_dict() for amenity in Myobj_place.amenities]
    else:
        Myobj = [storage.get(Amenity, amenity_id).to_dict()
                 for amenity_id in Myobj_place.amenity_ids]
    return jsonify(Myobj)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """returns Amenity with code 201"""
    Myobj_place = storage.get(Place, place_id)

    if not Myobj_place:
        abort(404)

    Myobj_amenity = storage.get(Amenity, amenity_id)
    if not Myobj_amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if Myobj_amenity in Myobj_place.amenities:
            return make_response(jsonify(Myobj_amenity.to_dict()), 200)
        Myobj_place.amenities.append(Myobj_amenity)
    else:
        if amenity_id in Myobj_place.amenity_ids:
            return make_response(jsonify(Myobj_amenity.to_dict()), 200)
        Myobj_place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(Myobj_amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """returns empty dict with code 200"""

    Myobj_place = storage.get(Place, place_id)
    if not Myobj_place:
        abort(404)

    Myobj_amenity = storage.get(Amenity, amenity_id)
    if not Myobj_amenity:
        abort(404)

    for elm in Myobj_place.amenities:
        if elm.id == Myobj_amenity.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                Myobj_place.amenities.remove(Myobj_amenity)
            else:
                Myobj_place.amenity_ids.remove(Myobj_amenity)
            storage.save()

            return make_response(jsonify({}), 200)
