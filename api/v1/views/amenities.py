#!/usr/bin/python3
"""_summary_
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/amenities", strict_slashes=False)
def all_amenities():
    amenities = storage.all(Amenity)
    amenities_list = []

    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>")
def one_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delets_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    try:
        data = request.get_json()

        if not data:
            abort(400, description="Not a JSON")

        if "name" not in data:
            abort(400, description="Missing name")

        instance = Amenity(**data)
        instance.save()
        return jsonify(instance.to_dict()), 201

    except Exception as e:
        abort(400, description="Not a JSON")


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    ignore = ["id", "created_at", "updated_at"]

    if not amenity:
        abort(404)

    try:
        data = request.get_json()

        if not amenity:
            abort(404)
        if not data:
            abort(400, description="Not a JSON")

        for key, value in data.items():
            if key not in ignore:
                setattr(amenity, key, value)

        storage.save()
        return jsonify(amenity.to_dict()), 200

    except Exception as e:
        abort(400, description="Not a JSON")
