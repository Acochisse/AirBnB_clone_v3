#!/usr/bin/python3
"""new view for places_reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<places_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_reviews(places_id):
    """retrieves a list of all place objects"""
    if request.method == "GET":
        all_places = []
        place_info = storage.get(Place, places_id)

        if place_info is not None:
            for key in place_info.reviews:
                all_places.append(key.to_dict())
            return jsonify(all_places)
        abort(404)

    if request.method == 'POST':
        if not request.is_json:
            return "Not a JSON", 400

        place_info = storage.get(Place, places_id)
        if place_info is not None:
            kwargs = {"place_id": places_id}
            kwargs.update(request.get_json())
            all_places = Review(**kwargs)
            dict_info = all_places.to_dict()

            if "user_id" not in dict_info.keys():
                return "Missing user_id", 400

            if not storage.get(User, dict_info.get("user_id")):
                abort(404)

            if "text" not in dict_info.keys():
                return "Missing text", 400

            all_places.save()
            return jsonify(all_places.to_dict()), 201
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def review_ident(review_id):
    """"updates a review object"""
    if request.method == "GET":
        review_info = storage.get(Review, review_id)
        if review_info is not None:
            return jsonify(review_info.to_dict())
        abort(404)

    if request.method == "PUT":
        review_info = storage.get(Review, review_id)
        ignoreKeys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        if review_info is not None:
            if not request.is_json:
                return "Not a JSON", 400

            for key, value in request.get_json().items():
                if key not in ignoreKeys:
                    setattr(review_info, key, value)
            storage.save()
            return jsonify(review_info.to_dict()), 200
        abort(404)

    if request.method == "DELETE":
        review_info = storage.get(Review, review_id)
        if review_info is not None:
            review_info.delete()
            storage.save()
            return jsonify({}), 200
        abort(404)
