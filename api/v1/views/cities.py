#!/usr/bin/python3
"""_summary_
"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


# @app_views.route("/cities", strict_slashes=False, methods=["GET"])
# def get_all_cities():
#     """Get All cities objects"""

#     list_cities = []
#     cities = storage.all(City)
#     for city in cities.values():
#         list_cities.append(city.to_dict())

#     return jsonify(list_cities)


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_sepcific_cities(state_id):
    """Get All Cities realted to Specific State"""

    state = storage.get(State, state_id)
    list_cities = []
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route("/cities/<city_id>/", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """Get a city object by ID"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def del_city(city_id):
    """Delete a city object by ID"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """Create a new city object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        data = request.get_json()

        if not data:
            abort(400, description="Not a JSON")

        if "name" not in data:
            abort(400, description="Missing name")

        city = City(**data)
        city.state_id = state.id
        city.save()
        return jsonify(city.to_dict()), 201

    except Exception as e:
        abort(400, description="Not a JSON")


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """Update a city object"""

    city = storage.get(City, city_id)
    ignore = ["id", "state_id", "created_at", "updated_at"]

    if not city:
        abort(404)

    try:
        data = request.get_json()

        if not data:
            abort(400, description="Not a JSON")

        for key, value in data.items():
            if key not in ignore:
                setattr(city, key, value)

        storage.save()
        return jsonify(city.to_dict()), 200

    except Exception as e:
        abort(400, description="Not a JSON")
