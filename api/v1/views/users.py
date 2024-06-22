#!/usr/bin/python3
"""_summary_
"""
from models import storage
from models.user import User
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_all_users():
    """Get All Users objects"""

    list_users = []
    users = storage.all(User)
    for user in users.values():
        list_users.append(user.to_dict())

    return jsonify(list_users)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """Get a User object by ID"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def del_user(user_id):
    """Delete a User object by ID"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """Create a new User object"""

    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Update a User object"""

    user = storage.get(User, user_id)
    data = data = request.get_json()
    ignore = ["id", "email", "created_at", "updated_at"]

    if not user:
        abort(404)
    elif not data:
        abort(400, description="Not a JSON")
    else:
        for key, value in data.items():
            if key not in ignore:
                setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
