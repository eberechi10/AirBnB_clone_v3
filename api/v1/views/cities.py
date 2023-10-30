#!/usr/bin/python3
""" Module containing cities for the API."""

from models import storage
from models.city import City
from models.state import State
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """gets City list objects of a State"""
    Myobj_state = storage.get(State, state_id)

    if not Myobj_state:
        abort(404)
    return jsonify([city.to_dict() for city in Myobj_state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def single_city(city_id):
    """gets City object"""
    Myobj = storage.get(City, city_id)
    if not Myobj:
        abort(404)
    return jsonify(Myobj.to_dict())


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Returns new City with code 201"""
    Myobj_state = storage.get(State, state_id)

    if not Myobj_state:
        abort(404)

    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")

    if 'name' not in new_city:
        abort(400, "Missing name")

    Myobj = City(**new_city)
    setattr(Myobj, 'state_id', state_id)
    storage.new(Myobj)
    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Returns emptydict with code 200"""
    Myobj = storage.get(City, city_id)

    if not Myobj:
        abort(404)
    Myobj.delete()

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Returns City object"""
    Myobj = storage.get(City, city_id)
    if not Myobj:
        abort(404)

    elm = request.get_json()
    if not elm:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'created_at', 'update_at', 'state_id']:
            setattr(Myobj, key, value)

    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 200)
