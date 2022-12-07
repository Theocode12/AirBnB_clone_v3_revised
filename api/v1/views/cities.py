#!/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage
from datetime import datetime

@app_views.route('/states/<state_id>/cities')
def state_cities(state_id):
    """Retrieves all the cities belonging to a state"""
    all_cities = []
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    cities_objs = state_obj.cities
    for city_obj in cities_objs:
        all_cities.append(city_obj.to_dict())

    return jsonify(all_cities)

@app_views.route('/cities/<city_id>', methods=['GET'])
def city(city_id):
    """Retrieves a city object"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a city object"""
    if not storage.get(State, state_id):
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        abort(400, jsonify(message='Not a JSON'))
    obj_dict = request.get_json()
    if not obj_dict.get('name'):
        abort(400, jsonify(message='Missing name'))
    city_obj = City()
    city_obj.state_id = state_id
    city_obj.name = obj_dict.get('name')
    storage.new(city_obj)
    storage.save()
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """updates city object"""
    skip_keys = {'id', 'created_at', 'updated_at'}
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        abort(400, jsonify(message='Not a JSON'))
    obj_dict = request.get_json()
    for key, value in obj_dict.items():
        if key not in skip_keys:
            setattr(city_obj, key, value)
            setattr(city_obj, 'updated_at', datetime.utcnow())
    storage.save()
    return jsonify(city_obj.to_dict())
