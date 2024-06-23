#!/usr/bin/python3
"""_summary_
"""
from flask import jsonify
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, User, City, Review, State, Place]
    strings = ["amenities", "users", "cities", "reviwes", "states", "places"]
    dict1 = {}

    for i in range(len(classes)):
        dict1[strings[i]] = storage.count(classes[i])

    return jsonify(dict1)
