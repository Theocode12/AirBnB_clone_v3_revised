#!/usr/bin/python3

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request
from datetime import datetime

@app_views.route('/states/', strict_slashes=False)
def all_states():
    """Retrives all states in the database"""
    states_dict = []
    state_objs = storage.all(State).values()
    for obj in state_objs:
        states_dict.append(obj.to_dict())
    return jsonify(states_dict)

@app_views.route('/states/<state_id>', methods=['GET'])
def one_state(state_id):
    """Retrives a state from the id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    return jsonify(state_obj.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes states with using the id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a new state object"""
    if request.headers['Content-Type'] != 'application/json':
        abort(400, 'Not a JSON')
    obj_dict = request.get_json()
    if not obj_dict.get('name'):
        abort(400, "Missing name")
    state_obj = State()
    state_obj.name = obj_dict.get('name')
    storage.new(state_obj)
    storage.save()
    return jsonify(state_obj.to_dict())

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state object"""
    skip_keys = {'id', 'created_at', 'updated_at'}
    if request.headers['Content-Type'] != 'application/json':
        abort(400, 'Not a JSON')
    obj_dict = request.get_json()
    state_obj = storage.get(State, state_id)
    for key, value in obj_dict.items():
        if key not in skip_keys:
            setattr(state_obj, key, value)
            setattr(state_obj, 'updated_at', datetime.utcnow())
    storage.save()
    return jsonify(state_obj.to_dict())
    
