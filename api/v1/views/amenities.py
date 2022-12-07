#!/usr/bin/python3

from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from datetime import datetime

@app_views.route('/amenities')
def all_amenity():
    """Retrieve all amenity object"""
    amenities_dict = []
    amenity_objs = storage.all(Amenity).values()
    for obj in amenity_objs:
        amenities_dict.append(obj.to_dict())
    return jsonify(amenities_dict)

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def one_amenity(amenity_id):
    """Retrieve one amenity using its id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete amenity using its id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create an amenity object"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    obj_dict = request.get_json()
    if not obj_dict.get('name'):
        abort(400, "Missing name")
    amenity_obj = Amenity()
    amenity_obj.name = obj_dict.get('name')
    storage.new(amenity_obj)
    storage.save()
    return jsonify(amenity_obj.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update an amenity object"""
    skip_keys = {'id', 'created_at', 'updated_at'}
    if not request.is_json:
        abort(400, 'Not a JSON')
    obj_dict = request.get_json()
    amenity_obj = storage.get(Amenity, amenity_id)
    for key, value in obj_dict.items():
        if key not in skip_keys:
            setattr(amenity_obj, key, value)
            setattr(amenity_obj, 'updated_at', datetime.utcnow())
    storage.save()
    return jsonify(amenity_obj.to_dict())
