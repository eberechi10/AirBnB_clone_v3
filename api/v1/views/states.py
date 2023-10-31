#!/usr/bin/python3
"""module to ontain states view for the API."""

from models import storage

from models.state import State
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """gets the State objects"""

    Myobjs = storage.all(State)
    return jsonify([Myobj.to_dict() for Myobj in Myobjs.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """gets the State object"""

    Myobj = storage.get(State, state_id)
    if not Myobj:
        abort(404)
    return jsonify(Myobj.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """Deletes the State object"""

    Myobj = storage.get(State, state_id)
    if not Myobj:
        abort(404)

    Myobj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """returns new State with code 201"""
    new_obj = request.get_json()
    if not new_obj:
        abort(400, "Not a JSON")

    if 'name' not in new_obj:
        abort(400, "Missing name")

    Myobj = State(**new_obj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates the State object """

    Myobj = storage.get(State, state_id)
    if not Myobj:
        abort(404)

    elm = request.get_json()
    if not elm:
        abort(400, "Not a JSON")

    for key, value in elm.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(Myobj, key, value)

    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 200)
