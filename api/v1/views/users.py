#!/usr/bin/python3

from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views
from datetime import datetime

@app_views.route('/users')
def all_users():
    """Retrieve all users object"""
    users_dict = []
    user_objs = storage.all(User).values()
    for obj in user_objs:
        users_dict.append(obj.to_dict())
    return jsonify(users_dict)

@app_views.route('/users/<user_id>', methods=['GET'])
def one_user(user_id):
    """Retrieve one user using its id"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user using its id"""
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create an user object"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    obj_dict = request.get_json()
    if not obj_dict.get('email'):
        abort(400, "Missing email")
    if not obj_dict.get('password'):
        abort(400, 'Missing password')
    user_obj = User()
    for key, value in obj_dict.items():
        setattr(user_obj, key, value)
    storage.new(user_obj)
    storage.save()
    return jsonify(user_obj.to_dict())

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update an user object"""
    skip_keys = {'id', 'created_at', 'updated_at', 'email'}
    if not request.is_json:
        abort(400, 'Not a JSON')
    obj_dict = request.get_json()
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    for key, value in obj_dict.items():
        if key not in skip_keys:
            setattr(user_obj, key, value)
            setattr(user_obj, 'updated_at', datetime.utcnow())
    storage.save()
    return jsonify(user_obj.to_dict())
