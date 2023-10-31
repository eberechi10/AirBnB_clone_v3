#!/usr/bin/python3
"""module that ontains users view for the API."""

from models import storage
from models.user import User

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """gets all User objects"""

    Myobjs = storage.all(User)
    return jsonify([Myobj.to_dict() for Myobj in Myobjs.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """gets a User object"""

    Myobj = storage.get(User, user_id)

    if not Myobj:
        abort(404)
    return jsonify(Myobj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """gets empty dict with code 200"""

    Myobj = storage.get(User, user_id)
    if not Myobj:
        abort(404)

    Myobj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """returns new User with the code 201"""

    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")

    if 'email' not in new_user:
        abort(400, "Missing email")

    if 'password' not in new_user:
        abort(400, 'Missing password')

    Myobj = User(**new_user)
    storage.new(Myobj)

    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """returns User object with ode 200"""

    Myobj = storage.get(User, user_id)
    if not Myobj:
        abort(404)

    elm = request.get_json()
    if not elm:
        abort(400, "Not a JSON")

    for key, value in elm.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(Myobj, key, value)

    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 200)
