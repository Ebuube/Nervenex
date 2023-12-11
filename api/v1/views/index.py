#!/usr/bin/python3
""" Index """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = {'User': User}

    num_objs = {}
    for key, val in classes.items():
        num_objs[key] = storage.count(val)

    return jsonify(num_objs)
