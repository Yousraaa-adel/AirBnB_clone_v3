#!/usr/bin/python3
"""_summary_
"""
# api/v1/views/index.py
from flask import jsonify
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route("/status", methods=["GET"])
def get_status():
    return {"status": "OK"}


@app_views.route("/stats", methods=["GET"])
def get_stats():
    # classes = [Amenity, User, City, Review, State, Place]
    # strings = ["amenities", "users", "cities", "reviwes", "states", "places"]

    # classes = {"amenities": Amenity, "cities": City,
    #     "places": Place, "reviwes": Review, "states": State, "users": User}
    # dict1 = {}

    # for key, value in classes.items():
    #     x = storage.count(value)
    #     dict1[key] = x
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviwes = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)

    return {"amenities": amenities,
            "cities": cities,
            "places": places,
            "reviews": reviwes,
            "states": states,
            "users": users}
