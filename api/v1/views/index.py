#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
                   "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status")
def index():
    return jsonify({'status':'OK'})


@app_views.route('/stats')
def object_numbers():
    """counts the number of each objects by type"""
    objs_count = {}

    for name, cls in classes.items():
        obj_count = storage.count(cls)
        objs_count[name] = obj_count

    return jsonify(objs_count)


