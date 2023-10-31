#!/usr/bin/python3
''' module that contains amenities for the API.'''

from api.v1.views import app_views
from models import storage

from models.amenity import Amenity
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """builds list of Amenity objects"""
    Myobjs = storage.all(Amenity)
    return jsonify([Myobj.to_dict() for Myobj in Myobjs.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def single_amenities(amenity_id):
    """Retrieves a Amenity object"""
    Myobj = storage.get(Amenity, amenity_id)

    if not Myobj:
        abort(404)
    return jsonify(Myobj.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenities(amenity_id):
    """empty dictionary with code 200"""

    Myobj = storage.get(Amenity, amenity_id)
    if not Myobj:
        abort(404)

    Myobj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Returns new Amenity"""
    new_amenity = request.get_json()

    if not new_amenity:
        abort(400, "Not a JSON")

    if 'name' not in new_amenity:
        abort(400, 'Missing name')

    Myobj = Amenity(**new_amenity)
    storage.new(Myobj)
    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Returns Amenity object"""
    Myobj = storage.get(Amenity, amenity_id)

    if not Myobj:
        abort(404)

    elm = request.get_json()
    if not elm:
        abort(400, "Not a JSON")

    for key, value in elm.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(Myobj, key, value)

    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 200)
