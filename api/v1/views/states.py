#!/usr/bin/python3
"""_summary_
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/states/")
def all_states():
    states = storage.all(State)
    states_list = []

    for state in states.values():
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route("/states/<state_id>")
def one_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delets_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    try:
        data = request.get_json()

        if not request.is_json:
            abort(400, description="Not a JSON")

        if not data:
            abort(400, description="Not a JSON")

        if "name" not in data:
            abort(400, description="Missing name")

        instance = State(**data)
        instance.save()
        return jsonify(instance.to_dict()), 201

    except Exception as e:
        abort(400, description="Not a JSON")


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    state = storage.get(State, state_id)
    ignore = ["id", "created_at", "updated_at"]

    if not state:
        abort(404)

    try:
        data = request.get_json()

        if not data:
            abort(400, description="Not a JSON")

        for key, value in data.items():
            if key not in ignore:
                setattr(state, key, value)

        storage.save()
        return jsonify(state.to_dict()), 200

    except Exception as e:
        abort(400, description="Not a JSON")
