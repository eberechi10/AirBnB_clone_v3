#!/usr/bin/python3
"""module containing places_reviews view for the API."""

from api.v1.views import app_views
from models import storage
from models.place import Place

from models.review import Review
from models.user import User

from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review(place_id):
    """gets all review objects of a Place"""

    Myobj_place = storage.get(Place, place_id)
    if not Myobj_place:
        abort(404)
    return jsonify([obj.to_dict() for Myobj in Myobj_place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def single_review(review_id):
    """gets a Review object"""
    Myobj = storage.get(Review, review_id)
    if not Myobj:
        abort(404)
    return jsonify(Myobj.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def push_review(place_id):
    """returns new review with code 201"""

    Myobj_place = storage.get(Place, place_id)
    if not Myobj_place:
        abort(404)

    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")

    if 'user_id' not in new_review:
        abort(400, "Missing user_id")
    user_id = new_review['user_id']

    Myobj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)

    if 'text' not in new_review:
        abort(400, "Missing text")

    Myobj = Review(**new_review)
    setattr(Myobj, 'place_id', place_id)
    storage.new(Myobj)
    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """returns empty dict with code 200"""

    Myobj = storage.get(Review, review_id)
    if not Myobj:
        abort(404)
    Myobj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """returns review object with code 200"""

    Myobj = storage.get(Review, review_id)
    if not Myobj:
        abort(404)

    elm = request.get_json()
    if not elm:
        abort(400, "Not a JSON")

    for k, vaiue in elm.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(Myobj, k, value)

    storage.save()
    return make_response(jsonify(Myobj.to_dict()), 200)
